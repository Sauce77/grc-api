from rest_framework import serializers

from extraccion.models import Registro
from extraccion.serializers import GetAplicativoSerializer

class PostRespuestaSerializer(serializers.ModelSerializer):

    app = serializers.CharField(max_length=100,required=True)

    class Meta:
        model = Registro
        fields = ["app","usuario","requiere_acceso","comentarios"]

class PostCuentasExentas(serializers.Serializer):
    """
        Serializa la cuentas exentas de bajas.
    """
    app = serializers.CharField(max_length=100,required=True)
    usuario = serializers.CharField(max_length=100,required=True)

class PostPoliticaUltimoAcceso(serializers.Serializer):
    """
        Serializa la peticion para realizar la politica
    """
    dias = serializers.IntegerField()
    apps = serializers.ListField(child=GetAplicativoSerializer())