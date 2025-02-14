from extraccion.models import Registro
from .asignacion import encontrarPerfil,encontrarAplicativo,encontrarResponsable
from extraccion.serializers import PostRegistroSerializer,DeleteRegistroSerializer

def leer_op_registros(data):
    """
        Utiliza la informacion recibida en el cuerpo del request
        para crear, actualizar y borrar los registros de la base
        de datos con respecto a la extraccion. 
    """
    registros = PostRegistroSerializer(data=data, many=True)

    if registros.is_valid():
        for registro in registros.validated_data:
            try:
                modificar_registro(registro)
            except :
                crear_registro(registro)

        return {"message": "Se ha actualizado la informacion."}


    return {"message": "Hay errores en la informacion ingresada."}

def crear_registro(validated_data):
    """
        Crea un registro a partir de los datos validados
        de un serializer (PostRegistroSerializer)
    """
    try:
        # obtenemos el area
        nombre_area = None
        # si existe el atributo area
        if "area" in validated_data:
            nombre_area = validated_data["area"]

        # obtenemos el perfil
        nombre_perfil = None
        # si existe el atributo perfil
        if "perfil" in validated_data:
            nombre_perfil = validated_data["perfil"]
        perfil = encontrarPerfil(nombre_perfil,nombre_area)

        # obtenemos el nombre del app
        nombre_app = validated_data["app"]
        # obtenemos el objeto del app
        app = encontrarAplicativo(nombre_app)

        # obtenemos el nombre del responsable
        nombre_responsable = validated_data["responsable"].upper()
        # obtenemos el objeto del responsable
        responsable = encontrarResponsable(nombre_responsable)

        # agregamos el nuevo registro
        Registro.objects.create(
            app = app,
            nombre = validated_data["nombre"],
            usuario = validated_data["usuario"],
            estatus = validated_data["estatus"],
            perfil = perfil,
            fecha_creacion = validated_data["fecha_creacion"],
            ultimo_acceso = validated_data["ultimo_acceso"],
            responsable = responsable
        )

    except NameError:
        return {"message": "No se pudo crear el registro."}
    
def modificar_registro(validated_data):
    """
        Modifica los campos de un registro ya existente, deberia
        solo modifcar el ultimo acceso, aunque se ejecutara la accion
        con cada campo.
    """
    # obtenemos el nombre del app
    nombre_app = validated_data["app"]
    # obtenemos el nombre de usuario del registro
    nombre_usuario = validated_data["usuario"]

    # obtenemos el registro
    obj_registro = Registro.objects.filter(app__nombre=nombre_app).get(usuario=nombre_usuario)
    obj_registro.ultimo_acceso = validated_data["ultimo_acceso"]
    obj_registro.en_extraccion = True
    obj_registro.save()

def borrar_op_registros(data):
    """
        Aquellos usuarios que no aparezcan en la extraccion serán borrados
        de la base de datos.
    """
    # almacena los errores al momento 
    messages = []

    registros = DeleteRegistroSerializer(data=data, many=True)

    if registros.is_valid(): 
        for registro in registros.validated_data:

            nombre_app = registro["app"]
            nombre_usuario = registro["usuario"]

            try:
                Registro.objects.filter(app=nombre_app).get(usuario=nombre_usuario).delete()
                messages.append(f"Usuario: {nombre_usuario} - App: {nombre_app}. Borrado.")
            except :
                messages.append(f"No se encontro {nombre_usuario} en {nombre_app}.")
        
    return messages
        


    