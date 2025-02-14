from django.urls import path

from .views import list_users, registro, login

urlpatterns = [
    path("users/", list_users, name="users"),
    path("registro/", registro, name="registro"),
    path("login/", login, name="login")
]
