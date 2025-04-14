from rest_framework import serializers

from extraccion.models import Registro
from extraccion.serializers import Aplicativo

class PostRespuestaSerializer(serializers.ModelSerializer):
    app = serializers.StringRelatedField()

    class Meta:
        model = Registro
        include = ["app","usuario","requiere_acceso","comentarios"]

        