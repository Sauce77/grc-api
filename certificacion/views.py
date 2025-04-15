from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser

from django.contrib.auth.models import User

from .serializers import PostRespuestaSerializer
from extraccion.serializers import GetRegistroSerializer

from extraccion.models import Registro, Responsable

def root(request):
    return "root"

# -------------------------- CERTIFICACION -----------------------

@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def enviar_certificacion_usuarios(request):
    """
        Recibe app y usuario de un usuario seleccionado.
    """
    # serializar contenido de request
    registros = PostRespuestaSerializer(data=request.data, many=True)

    if registros.is_valid():
        # para cada elemento a registrar
        for registro in registros.validated_data:
            try:
                obj_registro = Registro.objects.filter(app__nombre=registro["app"]).get(usuario=registro["usuario"])
                obj_registro.requiere_acceso = registro["requiere_acceso"]
                obj_registro.comentarios = registro["comentarios"]
                obj_registro.save()
            except Registro.DoesNotExist:
                return Response({"message": "Usuario cargado no existe."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({"message":"Certificacion enviada!"}, status=status.HTTP_200_OK)
    else:
        return Response({"message":"Formato de registros incorrecto!","errors": registros.errors}, status=status.HTTP_400_BAD_REQUEST)
    
# ---------------------- REGISTROS ----------------------

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def mostrar_usuario_registros(request,usuario):
    """
        Muestra los registros todos los registros asignados al usuario.
    """
    # obtenemos el usuario
    obj_usuario = User.objects.get(username=usuario)
    # obtenemos los responsables
    obj_responsables = Responsable.objects.filter(usuario=obj_usuario)
    # obtenemos responsables del usuario
    registros = Registro.objects.filter(responsable__in=obj_responsables).filter(en_extraccion=True)
    
    serializer = GetRegistroSerializer(registros, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def mostrar_usuario_app_registros(request,app,usuario):
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