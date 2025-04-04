from datetime import datetime,timedelta

from extraccion.models import Registro
from .asignacion import encontrarPerfil,encontrarAplicativo,encontrarResponsable
from extraccion.serializers import PostRegistroSerializer,DeleteRegistroSerializer

from extraccion.models import Registro

def crear_registro(validated_data):
    """
        Crea un registro a partir de los datos validados
        de un serializer (PostRegistroSerializer)
    """
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
    
def modificar_registro(validated_data):
    """
        Modifica los campos de un registro ya existente, deberia
        solo modifcar el ultimo acceso y responsable.
    """
    # obtenemos el nombre del app
    nombre_app = validated_data["app"]
    # obtenemos el nombre de usuario del registro
    nombre_usuario = validated_data["usuario"]

    # obtenemos el registro
    obj_registro = Registro.objects.filter(app__nombre=nombre_app).get(usuario=nombre_usuario)

    obj_registro.ultimo_acceso = validated_data["ultimo_acceso"]

    # obtenemos el responsable
    responsable = encontrarResponsable(validated_data["responsable"])
    obj_registro.responsable = responsable
    obj_registro.en_extraccion = True
    obj_registro.comentarios = None
    obj_registro.save()


def aplicar_exentar_bajas(cuentas_exentas):
    """
        Dado una lista con Aplictivo y Usuario. Modificara los campos
        requiere_acceso y comentarios para evadir la politica.
    """

    for cuenta in cuentas_exentas:
        # encontramos el registro
        registro = Registro.objects.filter(app__nombre=cuenta["app"]).get(username=cuenta["usuario"])
        # modificamos los campos
        registro.requiere_acceso = None
        registro.comentarios = None
        registro.save()

    return


def aplicar_politica_ultimo_acceso(apps,cuentas_exentas,dias_politica):
    """
        Considerando un periodo de tiempo, los usuario que rebasen este
        periodo tras su ultima conexion seran marcados como 
        requiere_acceso = NO.
        En caso de no contar con ultimo_acceso se toma en cuenta
        la fecha de creacion.
        Se deben especificar sobre que aplicativos.
    """

    # obtenemos la fecha hoy
    fecha_hoy = datetime.now()
    # obtenemos mes y anio
    fecha_mm_yyyy = fecha_hoy.strftime("%Y-%m")
    # establecemos el primer dia del mes
    fecha_primero = datetime.strptime(fecha_mm_yyyy + "-01", "%Y-%m-%d")
    # restamos_dias_politica
    fecha_politica = fecha_primero - timedelta(days=dias_politica)

    # obtenemos registros de las apps para politica
    registros = Registro.objects.filter(app__nombre__in=apps)


    # filtramos a los registros con ultimo acceso anterior a politica
    registros_ua = registros.exclude(ultimo_acceso=None).filter(ultimo_acceso__lt=fecha_politica)
    registros_ua.update(requiere_acceso="NO", comentarios=f"BAJA POLITICA {dias_politica} DIAS")

    # filtramos a los registros sin ultimo acceso con fecha de creacion previa a politica
    registros_fc = registros.filter(ultimo_acceso=None).filter(fecha_creacion__lt=fecha_politica)
    registros_fc.update(requiere_acceso="NO", comentarios=f"BAJA POLITICA {dias_politica} DIAS")

    aplicar_exentar_bajas(cuentas_exentas)
    return
    