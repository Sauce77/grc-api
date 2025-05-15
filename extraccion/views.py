from django.shortcuts import render,HttpResponse
from django.http import Http404
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from scripts.operaciones_registros import modificar_registro,crear_registro
from extraccion.serializers import PostRegistroSerializer, GetAplicativoSerializer, GetResponsableSerializer

# Create your views here.

from .models import Registro, Aplicativo, Responsable

from .serializers import GetRegistroSerializer,PostRegistroSerializer

def root(request):
    return(HttpResponse("root"))


# ----------------- APLICATIVOS --------------------
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def mostrar_all_apps(request):
    """
        Muestra los aplicativos registrados.
    """
    apps = Aplicativo.objects.all()
    serializer = GetAplicativoSerializer(apps, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def mostrar_usuario_apps(request,usuario):
    """
        Muestra los aplicativos pertenecientes a registros del usuario.
    """
    obj_responsables = Responsable.objects.filter(usuario__username=usuario)
    # obtenemos registros del responsable
    obj_registros = Registro.objects.filter(responsable__in=obj_responsables)
    # obtenemos app distintas
    apps_unicos = obj_registros.values('app').distinct()
    # filtramos las apps
    obj_apps = Aplicativo.objects.filter(id__in=apps_unicos)

    serializer = GetAplicativoSerializer(obj_apps, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# ------------------ RESPONSABLES -------------------
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def mostrar_all_responsables(request):
    """
        Muestra todos los responsables registrados.
    """
    responsables = Responsable.objects.all()
    serializer = GetResponsableSerializer(responsables, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def mostrar_usuario_responsables(request,usuario):
    """
        Muestra los Responsables asociados con el usuario.
    """
    # obtenemos los responsables del usuario
    responsables = Responsable.objects.filter(usuario__username=usuario)

    serializer = GetResponsableSerializer(responsables, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# --------------------- REGISTROS ---------------------
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def mostrar_all_registros(request):
    """
        Muestra todos los registros en la base de datos.
    """
    registros = Registro.objects.all()
    serializer = GetRegistroSerializer(registros, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def mostrar_app_registros(request,app):
    """
        Muestra los registros de una app.
    """
    registros = Registro.objects.filter(app__nombre=app)
    serializer = GetRegistroSerializer(registros, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# ----------------------- EXTRACCION ---------------------

@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def actualizar_registros(request):
    """
        Recibe una extraccion completa. Actualiza los datos ya existentes en la 
        base de datos y crea aquellos que no estan presentes.

        Para detectar los que no estan presentes, se recurre al atributo "en_extraccion",
        si es verdadero, el registro fue encontrado en la extraccion.
    """
    # reestablecemos los valores de requiere_acceso y comentarios (excluye exentas de bajas)
    Registro.objects.filter(exenta_baja=False).update(requiere_acceso=None, comentarios="No se encuentra en extraccion")
    # colocamos el estado "en_extraccion" como false
    Registro.objects.all().update(en_extraccion=False)

    # serializar contenido de request
    registros = PostRegistroSerializer(data=request.data, many=True)

    if registros.is_valid():
        # para cada elemento a registrar
        for registro in registros.validated_data:
            try:
                modificar_registro(registro)
            except Registro.DoesNotExist:
                crear_registro(registro)
            except ValueError:
                return Response({"message": "Campo en extraccion invalido"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({"message":"Extraccion cargada!"}, status=status.HTTP_200_OK)
    else:
        return Response({"message":"Formato de extraccion incorrecto!","errors": registros.errors}, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def mostrar_no_extraccion(request):
    """
        Muestra los registros cuyo atributo "en_extraccion"=False
        Esto quiere decir que no se encontraron en la extraccion
        mas reciente
    """
    registros = Registro.objects.filter(en_extraccion=False)
    serializer = GetRegistroSerializer(registros, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def mostrar_exentas_bajas(request):
    """
        Muestra los registros cuyo atributo "exentas_bajas"=True
        Esto quiere decir que son exentas a la politica o bajas de
        responsable
    """
    registros = Registro.objects.filter(exenta_baja=True)
    serializer = GetRegistroSerializer(registros, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def mostrar_registros_baja(request):
    """
        Muestra los registros cuyo atributo "requiere_acceso"="NO".
    """
    registros = Registro.objects.filter(requiere_acceso="NO")
    serializer = GetRegistroSerializer(registros, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def borrar_registros_baja(request):
    """
        Borra los registros no exentos de bajas cuyo valor de requiere_acceso sea NO.
    """
    # serializamos registros de la respuesta
    registros_serializer = GetRegistroSerializer(data=request.data, many=True)

    if registros_serializer.is_valid():
        
        for registro in registros_serializer.validated_data:
            try:
                # filtramos registros de la app y con la respuesta
                obj_registro_app = Registro.objects.filter(app__nombre=registro["app"]).filter(requiere_acceso=registro["requiere_acceso"])
                obj_registro = obj_registro_app.get(usuario=registro["usuario"])
                obj_registro.delete()
            except Registro.DoesNotExist:
                return Response({"message": f"El usuario {registro["app"]} - {registro["usuario"]} no fue encontrado."}, status=status.HTTP_404_NOT_FOUND)
            
        # si se iteraron todos los registros
        return Response({"message": "Registros borrados."}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({"message": "Formato incorrecto."}, status=status.HTTP_400_BAD_REQUEST)