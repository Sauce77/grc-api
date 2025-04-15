from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser

from .serializers import PostRespuestaSerializer

from extraccion.models import Registro

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