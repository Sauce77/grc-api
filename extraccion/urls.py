from django.urls import path

from . import views

urlpatterns = [
    path('', views.root),
    # --------- APLICATIVOS --------------------
    path('apps/', views.mostrar_all_apps, name="mostrar_all_apps"),
    path('apps/<str:usuario>/', views.mostrar_usuario_apps, name="mostrar_usuario_apps"),
    # ---------- RESPONSABLES -------------------
    path('responsables/', views.mostrar_all_responsables, name="mostrar_all_responsables"),
    path('responsables/<str:usuario>/', views.mostrar_usuario_responsables, name="mostrar_usuario_responsables"),
    # ---------- REGISTROS ----------------------
    path('registros/', views.mostrar_all_registros, name="mostrar_all_registros"),
    path("registros/<str:app>/", views.mostrar_app_registros, name="mostrar_app_registros"),
    path("registros/<str:app>/<str:usuario>/", views.mostrar_usuario_registros, name="mostrar_usuario_registros"),
    # ---------- POLITICAS ----------------------
    path('politica/', views.aplicar_politica_registros, name="aplicar_politica_registros"),
    path('exentar/', views.aplicar_exentas_bajas, name="aplicar_exentas_bajas"),
    # ---------- EXTRACCION -----------------------
    path("insertar/", views.actualizar_registros, name="actualizar_registros"),
    path("omitidos/", views.mostrar_no_extraccion, name="mostrar_no_extraccion"),
    path("exentas/", views.mostrar_exentas_bajas, name="mostrar_exentas_bajas"),
    # path("borrar/", views.borrar_registros, name="borrar_registros"),
]
