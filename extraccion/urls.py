from django.urls import path

from .views import root, mostrar_registros, actualizar_registros, mostrar_no_extraccion, borrar_registros, mostrar_all_registros

urlpatterns = [
    path('', root),
    path('all/', mostrar_all_registros, name="mostrar_all_registros"),
    path("registros/<str:app>/", mostrar_registros, name="mostrar_registros"),
    path("insertar/", actualizar_registros, name="actualizar_registros"),
    path("omitidos/", mostrar_no_extraccion, name="mostrar_no_extraccion"),
    path("borrar/", borrar_registros, name="borrar_registros"),
]
