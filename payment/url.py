# payment/urls.py

from django.urls import path
from . import views

urlpatterns = [
    #path('create/<int:producto_id>/', views.create_payment, name='create_payment'),
    path('success/', views.payment_success, name='payment_success'),
    path('cancel/', views.payment_cancel, name='payment_cancel'),
    path('pago_exitoso/', views.pago_exitoso, name='pago_exitoso'),
    path('pago_cancelado/', views.pago_cancelado, name='pago_cancelado'),
    path('generar_pago_paypal/', views.generar_pago_paypal, name='generar_pago_paypal'),
]
