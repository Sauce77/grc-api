from django.urls import path

from .views import list_users, registro, login, crear_admin

urlpatterns = [
    path("users/", list_users, name="users"),
    path("registro/", registro, name="registro"),
    path("login/", login, name="login"),
    path("newadmin/", crear_admin, name="newadmin"),
]
