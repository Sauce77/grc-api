from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from rest_framework.decorators import permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .serializers import UserSerializer,AdminSerializer

import os
# Create your views here.

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_users(request):
    """
        Enlista todos los usuarios registrados.
    """
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(["POST"])
def login(request):
    """
        Si encuentra al usuario en la bd, inicia sesion.
    """

    user = get_object_or_404(User, username=request.data["username"])
    if not user.check_password(request.data["password"]):
        return Response({"error:": "Invalid password !"}, status=status.HTTP_400_BAD_REQUEST)
    
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)

    return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
def registro(request):
    """
        Crea un usuario y genera un token.
    """
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        user = User.objects.get(username=serializer.data["username"])
        user.set_password(serializer.data["password"])
        user.save()

        token = Token.objects.create(user=user)
        return Response(
            {"token": token.key, "user": serializer.data}, status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def crear_admin(request):

    messages = []

    server_admin_key = os.environ.get("ADMIN_KEY")

    serializer = AdminSerializer(data=request.data)

    if serializer.is_valid():
        user_admin_key = serializer.validated_data.get("admin_key")
        
        messages.append("serializer valido")
        if user_admin_key == server_admin_key:

            messages.append("key accepted")

            username = serializer.validated_data.get("username")
            first_name = serializer.validated_data.get("first_name")
            last_name = serializer.validated_data.get("last_name")
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")
            # crear superuser
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_superuser(
                    username = username,
                    first_name = first_name,
                    last_name = last_name,
                    email = email
                )
                user.set_password(password)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        else: 
            messages.append("user already exists")
    else:
        messages.append(serializer.errors)
    
    return Response({"message":messages},status=status.HTTP_400_BAD_REQUEST)

