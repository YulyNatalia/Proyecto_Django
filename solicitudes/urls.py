# solicitudes/urls.py
from django.urls import path
from django.urls import path
from .views import login_view
from django.urls import path
from . import views

urlpatterns = [
     path('inventario/', views.inventario, name='inventario'),
    path('login/', login_view, name='login'),  # Agregar la URL de login
    path('registro/', views.registro, name='registro'),  # URL para el registro
    path('solicitar-material/', views.solicitar_material, name='solicitar_material'),
    path('editar/<int:id>/', views.editar_solicitud, name='editar_solicitud'),
    path('eliminar/<int:id>/', views.eliminar_solicitud, name='eliminar_solicitud'),
    # Otras URLs...
]