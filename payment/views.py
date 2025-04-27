import paypalrestsdk
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from orders.views import Pago
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.conf import settings


# Configuración PayPal Sandbox
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET,
})

@api_view(['POST'])
def generar_pago_paypal(request):
    pago_id = request.data.get('pago_id')

    if not pago_id:
        return Response({'detail': 'Falta el ID del pago'}, status=status.HTTP_400_BAD_REQUEST)

    pago = get_object_or_404(Pago, id=pago_id)
    pedido = pago.pedido

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": "http://localhost:8000/payment/success/",
            "cancel_url": "http://localhost:8000/payment/cancel/",
        },
        "transactions": [{
            "amount": {
                "total": f"{pedido.total:.2f}",
                "currency": "USD"
            },
            "description": f"Pago de pedido {pedido.id}"
        }]
    })

    if payment.create():
    # Buscar la URL de aprobación
        for link in payment.links:
            if link.rel == "approval_url":
                approval_url = str(link.href)
                pago.paypal_payment_id = payment.id  # <-- Guarda aquí
                pago.save()
                return Response({'approval_url': approval_url}, status=status.HTTP_200_OK)

        return Response({'detail': 'No se encontró URL de aprobación'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'detail': 'Error creando el pago en PayPal', 'error': payment.error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def payment_success(request):
    return JsonResponse({'message': 'Pago exitoso'})

def payment_cancel(request):
    return JsonResponse({'message': 'Pago cancelado'})

@api_view(['GET'])
def pago_exitoso(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    if not payment_id or not payer_id:
        return Response({'detail': 'Datos incompletos en la respuesta de PayPal'}, status=status.HTTP_400_BAD_REQUEST)

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        # Aquí puedes buscar tu pago interno y marcarlo como pagado
        # (puedes guardar payment_id como referencia cuando generaste el pago)
        
        # Opcional: Si guardaste el payment_id de PayPal en tu modelo Pago
        pago = Pago.objects.filter(paypal_payment_id=payment_id).first()
        if pago:
            pago.estado = 'pagado'
            pago.save()
            pedido = pago.pedido
            pedido.estado = 'procesado'
            pedido.save()

        # Redireccionar a una página bonita
        return redirect('https://tutienda.com/checkout/success')  # <-- cambia esta URL
    else:
        return Response({'detail': 'No se pudo confirmar el pago en PayPal', 'error': payment.error}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def pago_cancelado(request):
    # Aquí puedes redirigir a un mensaje de cancelación
    return redirect('https://tutienda.com/checkout/cancel')  # <-- cambia esta URL
