from django.urls import path
from .views import RegistrarInteraccionView

urlpatterns = [
    path('registrar-interaccion/', RegistrarInteraccionView.as_view()),
]
