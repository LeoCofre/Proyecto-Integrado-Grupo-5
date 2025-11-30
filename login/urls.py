from django.urls import path
from . import views  # Importamos las vistas desde LA MISMA carpeta (login)

urlpatterns = [
    # Ruta para crear usuarios (Tu vista nueva)
    path('login', views.login_view, name='login'),
    path('crear-usuario/', views.crear_usuario_view, name='crear_usuario'),
    path('logout/', views.logout_view, name='logout'),
]