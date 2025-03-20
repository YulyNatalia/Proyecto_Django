# solicitudes/models.py
from django.db import models

class Solicitud(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, default='pendiente')

    def __str__(self):
        return self.nombre
    
class SolicitudMaterial(models.Model):
    nombre_solicitante = models.CharField(max_length=100)
    tipo_material = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    comentarios = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Solicitud de {self.nombre_solicitante} - {self.tipo_material}"
    