from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Aplicativo(models.Model):
    """
        Define una aplicacion de la empresa
    """
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre
    
class Area(models.Model):
    """
        Define un area asignada a un perfil
    """
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre
    
class Perfil(models.Model):
    """
        Define un perfil asignado en un aplicativo
    """
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(null=True, blank=True)

    area = models.ForeignKey(Area, null=True, blank=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nombre
    
class Responsable(models.Model):
    """
        Define quien es responsable de dicho registro
    """
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    correo = models.CharField(max_length=250, null=True, blank=True)
    usuario = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.nombre

class Registro(models.Model):
    """
        Define un usuario de un aplicativo
    """
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    usuario = models.CharField(max_length=100)
    estatus = models.CharField(max_length=25, default="Activo")
    fecha_creacion = models.DateField(null=True, blank=True)
    ultimo_acceso = models.DateField(null=True, blank=True)

    app = models.ForeignKey(Aplicativo, on_delete=models.DO_NOTHING)
    perfil = models.ForeignKey(Perfil, null=True, blank=True, on_delete=models.DO_NOTHING)
    responsable = models.ForeignKey(Responsable, on_delete=models.DO_NOTHING)

    requiere_acceso = models.CharField(max_length=15,null=True, blank=True)
    comentarios = models.TextField(null=True, blank=True)

    en_extraccion = models.BooleanField(default=True)
    exenta_baja = models.BooleanField(default=False)
    enviado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
