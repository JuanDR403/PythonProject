from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Tablero(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    propietario = models.ForeignKey(User, on_delete=models.CASCADE)
    usuarios_permitidos = models.ManyToManyField(User, related_name='tableros_permitidos', blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Tarjeta(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    id_tablero = models.ForeignKey(Tablero, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    etiquetas = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Tarea(models.Model):
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('En Progreso', 'En Progreso'),
        ('Realizada', 'Realizada'),
        ('Aprobada', 'Aprobada'),
        ('Por Corregir', 'Por Corregir'),
    ]

    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')
    id_tarjeta = models.ForeignKey(Tarjeta, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.descripcion

class Comentario(models.Model):
    contenido = models.TextField()
    tarjeta = models.ForeignKey('Tarjeta', on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_comentario = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contenido
    
class Historial(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    accion = models.CharField(max_length=255)
    fecha = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f'{self.usuario.username} - {self.accion} - {self.fecha}'