from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
import random


class User(models.Model):
    ROLE_CHOICES = [
        ("guionista", "Guionista"),
        ("estandar", "Estándar"),
    ]

    username = models.CharField(max_length=50, unique=True, null=False)
    email = models.EmailField(max_length=80, unique=True, null=False)
    password = models.CharField(max_length=255, null=False)
    role = models.CharField(
        max_length=50, choices=ROLE_CHOICES, default="estandar", null=False
    )


class Pose(models.Model):
    gesto = models.CharField(max_length=100)

    def __str__(self):
        return self.gesto


class Guion(models.Model):
    titulo = models.CharField(max_length=200)
    genero = models.CharField(max_length=100)
    ubicacion_actores = models.TextField()
    pose_actores = models.ForeignKey(Pose, on_delete=models.CASCADE)
    dialogos = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo


class GuionHistorial(models.Model):
    guion = models.ForeignKey(Guion, on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=timezone.now)
    titulo = models.CharField(max_length=200)
    genero = models.CharField(max_length=200)
    ubicacion_actores = models.JSONField()
    pose_actores = models.ForeignKey(Pose, on_delete=models.CASCADE, null=True)
    dialogos = models.TextField()

    def __str__(self):
        return f"Historial de {self.guion.titulo} ({self.fecha})"
