from rest_framework import serializers

from .models import Aplicativo, Perfil, Responsable, Registro

class PostCuentasExentas(serializers.Serializer):
    """
        Serializa la cuentas exentas de bajas.
    """
    app = serializers.CharField(max_length=100,required=True)
    usuario = serializers.CharField(max_length=100,required=True)

class GetAplicativoSerializer(serializers.ModelSerializer):
    """
        Serializa la informacion de los aplicativos disponibles
    """
    class Meta:
        model = Aplicativo
        exclude = ["id"]

class PostPoliticaUltimoAcceso(serializers.Serializer):
    """
        Serializa la peticion para realizar la politica
    """
    dias = serializers.IntegerField()
    apps = serializers.ListField(child=GetAplicativoSerializer())

class GetResponsableSerializer(serializers.ModelSerializer):
    """
        Serializa la informaion de los responsables registrados.
    """

    class Meta:
        model = Responsable
        exclude = ["id"]

class PostRegistroSerializer(serializers.ModelSerializer):
    """
        Serializa la informacion para insertar un registro.
    """
    app = serializers.CharField(max_length=100,required=True)
    responsable = serializers.CharField(max_length=100,required=True)
    perfil = serializers.CharField(max_length=100,allow_blank=True,allow_null=True)

    class Meta:
        model = Registro
        exclude = ["id"]

class GetRegistroSerializer(serializers.ModelSerializer):
    """
        Serializa la informacion para mostrar un registro.
    """
    
    app = serializers.StringRelatedField()
    responsable = serializers.StringRelatedField()
    perfil = serializers.StringRelatedField()

    class Meta:
        model = Registro
        exclude = ["id"]

class DeleteRegistroSerializer(serializers.ModelSerializer):
    """
        Recopila el app y usuario que sera borrado.
    """
    app = serializers.CharField(max_length=100,required=True)

    class Meta:
        model = Registro
        fields = ["id","app","usuario"]
