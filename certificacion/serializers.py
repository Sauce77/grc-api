from rest_framework import serializers

from extraccion.models import Registro
from extraccion.serializers import Aplicativo

class PostRespuestaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Registro
        fields = ["app","usuario","requiere_acceso","comentarios"]

        