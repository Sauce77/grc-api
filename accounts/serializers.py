from rest_framework import serializers

from django.contrib.auth.models import User
from .models import Rol

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ["id","nombre"]

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["first_name","last_name","username", "email","password"]

class AdminSerializer(serializers.ModelSerializer):

    admin_key = serializers.CharField(max_length=100, read_only=True)
    class Meta:
        model = User
        fields = ["username","first_name","last_name","password","admin_key"]
        extra_kwargs = {'password': {'write_only': True}, 'admin_key': {'write_only': True}}