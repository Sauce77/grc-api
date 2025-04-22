from rest_framework import serializers

from extraccion.models import Registro
from extraccion.serializers import Aplicativo

class PostRespuestaSerializer(serializers.ModelSerializer):

    app = serializers.CharField(max_length=100,required=True)

    class Meta:
        model = Registro
        fields = ["app","usuario","requiere_acceso","comentarios"]

        