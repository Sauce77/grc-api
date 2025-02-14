from django.contrib import admin

# Register your models here.
from .models import Aplicativo, Perfil, Area, Responsable, Registro

admin.site.register(Aplicativo)
admin.site.register(Perfil)
admin.site.register(Area)
admin.site.register(Responsable)
admin.site.register(Registro)