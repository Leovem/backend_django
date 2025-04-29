from django.urls import path
from .views import RegistroView, LoginView, EditarUsuarioView

urlpatterns = [
    path('register/', RegistroView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('editar/<int:id>/', EditarUsuarioView.as_view(), name='editar_usuario'),
]
