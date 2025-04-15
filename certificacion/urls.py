from django.urls import path

from . import views

urlpatterns = [
    path('', views.root),
    # ---------------- CERTIFICACION ---------------------
    path('enviar/', views.enviar_certificacion_usuarios, name="enviar_certificacion_usuarios"),
    #---------------- REGISTROS ---------------------------
    path("registros/user/<str:usuario>/", views.mostrar_usuario_registros, name="mostrar_usuario_registros"),
    path("registros/<str:app>/<str:usuario>/", views.mostrar_usuario_app_registros, name="mostrar_usuario_app_registros"),
]