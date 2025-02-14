from extraccion.models import Registro,Aplicativo,Perfil,Area,Responsable

def encontrarAplicativo(app):
    """
        Retorna el objeto del aplicativo. En caso de no encontrarlo
        lo crea.
    """
    try: 
        return Aplicativo.objects.get(nombre=app)
    except Aplicativo.DoesNotExist:
        obj_app = Aplicativo.objects.create(nombre=app)
        return obj_app
    
def encontarArea(area):
    """
        Retorna el objeto area. En caso de no encontrarlo lo crea.
    """
    if area == None:
        return None
    
    try:
        return Area.objects.get(nombre=area)
    except Area.DoesNotExist:
        obj_area = Area.objects.create(nombre=area)
        return obj_area
    
def encontrarPerfil(perfil,area):
    """
        Retorna el objeto perfil. En caso de no encontrarlo lo crea.
    """
    if perfil == None:
        return None

    try: 
        return Perfil.objects.get(nombre=perfil)
    
    except Perfil.DoesNotExist:
        # ubicamos el area a la que pertenece
        obj_area = encontarArea(area)
        if obj_area == None:
            obj_perfil = Perfil.objects.create(nombre=perfil)
        else:
            obj_perfil = Perfil.objects.create(nombre=perfil,area=obj_area)
        return obj_perfil
    
def encontrarResponsable(responsable):
    """
        Retorna el objeto responsable. En caso de no encontrarlo lo crea.
    """
    try: 
        return Responsable.objects.get(nombre=responsable)
    
    except Responsable.DoesNotExist:
        obj_responsable = Responsable.objects.create(nombre=responsable)
        return obj_responsable
    

