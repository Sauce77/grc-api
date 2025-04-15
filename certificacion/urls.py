from django.urls import path

from . import views

urlpatterns = [
    path('', views.root),
    path('enviar/', views.enviar_certificacion_usuarios, name="enviar_certificacion_usuarios"),
]