from django.apps import apps
from typing import Type
from .models import *
import re
from itertools import groupby

def get_all_furniture_models():
    """Получение всех моделей, что наследуются от абстрактного класса Furniture

    Returns:
        list: список всех моделей, что наследуются от абстрактного класса Furniture
    """
    models = filter(lambda model: issubclass(model, Furniture), apps.get_models())

    return list(models)

def get_all_AMain_models():
    """Получение всех моделей, что наследуются от абстрактного класса AMain
    
    Returns:
        list: список всех поделей, что наследуются от абстракного класса AMain"""
    
    models = filter(lambda model: issubclass(model, AMain), apps.get_models())

    return list(models)

def get_model_not_auto_created_fields(model: Type[models.Model]):
    """Получение тех полей модели, которые были написаны вручную, а не сгенерированы.

    Args:
        model (Type[models.Model]): класс модели

    Returns:
        list: список вручную написанных полей модели
    """
    fields = model._meta.get_fields(include_parents=False, include_hidden=False)
    not_auto_created_fields = list(filter(lambda field: not field.auto_created, fields))
    return list(not_auto_created_fields)

def reorder_furniture_fields(model_fields: list):
    """Перестановка полей наследуемого абстрактного класса в конец списка всех полей.

    Args:
        model_fields (list): список всех полей модели

    Returns:
        list: список с изменённым порядком полей и без поля id категории
    """
    furniture_fields = list(Furniture._meta.get_fields(include_parents=False, include_hidden=False))
    model_fields = model_fields[len(furniture_fields)::]
    model_fields = model_fields.__add__(furniture_fields)

    return model_fields

def reorder_compose_fields(model_fields: list):
    """Перестановка полей наследуемого абстрактного класса в конец списка всех полей.

    Args:
        model_fields (list): список всех полей модели

    Returns:
        list: список с изменённым порядком полей и без поля id категории
    """
    furniture_fields = list(Compose._meta.get_fields(include_parents=False, include_hidden=False))
    model_fields = model_fields[len(furniture_fields)::]
    model_fields = model_fields.__add__(furniture_fields)

    return model_fields[1::]

def get_furnitures(category_obj: Category = None, include_category:bool = False) -> dict:
    """Получение всех моделей, что наследуются от абстрактного класса Furniture, по их категории, если она указана
    
    Также в списке переставляются поля наследованного класса в конец

    Args:
        category_obj (Category, optional): объект модели Category по которому производится отбор
        include_category (bool, optional): нужно-ли оставлять поле категории. По умолчанию False.

    Returns:
        dict: словарь со следующими ключами и значениями:

        'items' list: список записей 
        'fields' list: список полей 
        'is_compose' bool: является-ли запись модулем
    """
    items = []
    fields = []
    is_compose = False
    model = None
    getAllFields = True

    furniture_models = get_all_furniture_models()

    if category_obj is None:
        for furniture_model in furniture_models:
            furniture_objects = furniture_model.objects.all()
            items.append(furniture_objects)

        return {
            'items_list': items
        }

    for furniture_model in furniture_models:
        furniture_objects = furniture_model.objects.filter(category=category_obj)

        is_compose = is_composable(furniture_model)
        model = furniture_model

        if len(furniture_objects) > 0:         
            items = furniture_objects
            fields = get_model_not_auto_created_fields(furniture_model)
            fields = reorder_furniture_fields(fields)

            if category_obj is not Other:
                for field in fields:
                    if field.name == 'ID_COMPONENT':
                        getAllFields = False
                        

            if not include_category:
                if getAllFields:
                    fields = list(filter(lambda field: field.name != 'category', fields))
                else:
                    fields = list(filter(lambda field: field.name == 'ID_COMPONENT' or 
                                                       field.name == "MFR_PART_NUM" or
                                                       field.name == "Package"      or 
                                                       field.name == "PCS"          or
                                                       field.name == "BOX"          or 
                                                       field.name == "Description", fields))
            break

    return {
        'items': items,
        'fields': fields,
        'is_compose': is_compose,
        'model': model
    }

def get_AMains_by_id_component(id_component: int)-> dict:
    """ Получение модели наследумой от AMain по id_component

    Returns:
        dict: словарь модели
        'object' - полученный объект
        'fields' - строки
        'model' - модель объекта 
    """

    model = None
    object = None
    fields = None

    AMain_models = get_all_AMain_models()

    for AMain_model in AMain_models:

        try:
            AMain_object = AMain_model.objects.get(ID_COMPONENT = id_component)

            object = AMain_object
            model = AMain_model

            fields = get_model_not_auto_created_fields(AMain_model)
            fields = reorder_furniture_fields(fields)


            if object is Other:
                fields = list(filter(lambda field:  field.name != 'category',   fields))
            else:
                fields = list(filter(lambda field:  field.name == 'ID_COMPONENT' or 
                                                    field.name == "MFR_PART_NUM" or
                                                    field.name == "Package"      or 
                                                    field.name == "PCS"          or
                                                    field.name == "BOX"          or 
                                                    field.name == "Description", fields))
        
            break

        except:
            pass
    
    
    return {
        'object': object,
        'fields': fields,
        'model': model
    }






def group_list_by_category(items: list):
    grouped_items = []
    for key, group in groupby(items, lambda item: item.category):
        grouped_items.append({'category': key, 'items': list(group)})

    return grouped_items

def search_items(search: str, category: Category = None):
    found_items = []

    if category is not None:
        furnitures = get_furnitures(category)

        for item in furnitures['items']:
            for field in furnitures['fields']:
                val = getattr(item, field.name)
                if val is None:
                    pass
                match = re.search(search.lower(), str(val).lower())
                if match:
                    found_items.append(item)
                    break
                
        return {
            'found_items': found_items,
            'fields': furnitures['fields'],
            'is_compose': furnitures['is_compose'],
            'model': furnitures['model']
        }
    else:
        furnitures = get_furnitures(include_category=True)

        for items in furnitures['items_list']:
            for item in items:
                fields = get_model_not_auto_created_fields(item._meta.model)
                for field in fields:
                    val = getattr(item, field.name)
                    if val is None:
                        passa
                    match = re.search(search.lower(), str(val).lower())
                    if match:
                        found_items.append(item)
                        break

        return {'found_items': found_items}

def is_composable(model: Type[models.Model]) -> bool:
    if model is Module or model is PCB:
        return True
    return False

def get_composed_field(model_name:str):
    compose_model = apps.get_model('main', model_name+"Composition")

    fields = get_model_not_auto_created_fields(compose_model)
    fields = reorder_compose_fields(fields)
    return fields[0].attname

def get_compositions(model_name:str, composed_id:int):
    compose_model = apps.get_model('main', model_name+"Composition")
    comps = compose_model.objects.all()
    return list(filter(lambda comp: getattr(comp,model_name.lower()+"_id") == composed_id, comps))