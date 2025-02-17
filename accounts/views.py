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

    serializer = AdminSerializer(data=request.data)
    # verificamos la info del request
    if serializer.is_valid():
        # obtenemos el admin key del request
        admin_key = serializer["admin_key"]
        messages.append(f"admin key request: {admin_key}")
        # si el admin key coincide con la del entorno
        if admin_key == os.environ.get("ADMIN_KEY"):
            messages.append("Admin Key provided!")
            # si el nombre de usuario no existe
            if not User.objects.filter(username=serializer.data["username"]).exists():
                user = User.objects.create_superuser(
                    username = serializer["username"],
                    first_name = serializer["first_name"],
                    last_name = serializer["last_name"],
                    email = serializer["email"]
                )
                user.set_password(serializer["password"])
                user.save()

                token = Token.objects.create(user=user)
                return Response(
                    {"token": token.key, "user": serializer.data}, status=status.HTTP_201_CREATED
                )
            
            else:
                messages.append("Username already exists.")
    
    return Response({"message":messages},status=status.HTTP_400_BAD_REQUEST)

