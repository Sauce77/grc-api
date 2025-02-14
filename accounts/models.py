from django.db import models

from django.contrib.auth.models import User
# Create your models here.

class Rol(models.Model):
    """
        Identifica los privilegios de un usuario. UNUSED.
    """
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True,null=True)
    
    def __str__(self):
        return self.nombre