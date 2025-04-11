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
from scripts.operaciones_registros import modificar_registro,crear_registro,aplicar_politica_ultimo_acceso,aplicar_exentar_bajas
from extraccion.serializers import PostRegistroSerializer, GetAplicativoSerializer, GetResponsableSerializer, PostPoliticaUltimoAcceso, PostCuentasExentas

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

    serializer = GetAplicativoSerializer(apps_unicos, many=True)
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

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def mostrar_usuario_registros(request,app,usuario):
    """
        Muestra los registros de una app, solo los registros asignados.
    """
    # obtenemos responsables del usuario
    obj_responsables = Responsable.objects.filter(usuario__username=usuario)
    # filtramos los registros por app 
    registros = Registro.objects.filter(app__nombre=app)
    # filtramos por responsable
    registros = registros.filter(responsable__in=obj_responsables)
    # filtramos aparecen en extraccion
    registros = registros.filter(en_extraccion=True)
    
    serializer = GetRegistroSerializer(registros, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# ------------- POLITICAS --------------------------

@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def aplicar_politica_registros(request):
    """
        Recibe un json indicando los dias de politica y los
        aplicativos donde se aplica la politica.
    """
    peticion = PostPoliticaUltimoAcceso(data=request.data)

    if peticion.is_valid():
        dias_politica = peticion.validated_data["dias"]
        apps = peticion.validated_data["apps"]

        aplicar_politica_ultimo_acceso(apps=apps,dias_politica=dias_politica)
        return Response({"message": "Politica aplicada con exito!"},status=status.HTTP_200_OK)
    
    return Response({"message":"Formulario invalido.","errors": peticion.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def aplicar_exentas_bajas(request):
    """
        Recibe una lista de app-usuarios, estos usuarios modificaran
        su valor exenta_bajas a True.
    """
    cuentas = PostCuentasExentas(data=request.data,many=True)

    if cuentas.is_valid():
         messages = aplicar_exentar_bajas(cuentas.validated_data)
         return Response({"messages": messages},status=status.HTTP_200_OK)
    else:
        return Response(cuentas.errors, status=status.HTTP_400_BAD_REQUEST)

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
    # colocamos el estado "en_extraccion" como false
    Registro.objects.all().update(en_extraccion=False,comentarios="No se encuentra en extraccion.")

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

"""
@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def borrar_registros(request):

    messages = borrar_op_registros(request.data)
    return Response(messages, status=status.HTTP_204_NO_CONTENT)

"""