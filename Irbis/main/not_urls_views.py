from .models_fields import get_AMains_by_id_component,get_furnitures
from .models import *
from .forms import *

def module_detail_view(model):
    data = get_data()

    moduleCompositions = ModuleComposition.objects.filter(module = model)

    for moduleComposition in moduleCompositions:

        elements = PCBComposition.objects.filter(pcb = moduleComposition.pcb)

        data = get_all_connected_element(elements, data)

    data['file'] = model.stepFile

    return data

def pcb_detail_view(model):
    data = get_data()

    elements = PCBComposition.objects.filter(pcb = model)

    data = get_all_connected_element(elements, data)

    fields = data['element']['fields']

    _fields = list(filter(lambda field:  field.name == 'ID_COMPONENT' or
                                        field.name == 'MFR_PART_NUM' or
                                        field.name == 'Description'  or
                                        field.name == 'BOX', fields ))

    data['fields'] = _fields

    data['gbrs'] = None
    data['buildFiles'] = None

    return data

def search_model_by_pk(name, pk):
    category = Category.objects.get(name = name)
    model = get_furnitures(category)['model']
    return model.objects.get(pk = pk)

def get_all_connected_element(elements, data = None):
    data = get_data(data)

    for element in elements:
        if(element.element is None): continue

        AMain_item = get_AMains_by_id_component(element.element.pk)

        if AMain_item['object'] is None: continue

        data['element']['fields'] = AMain_item['fields']
        objects = data['element']['items']
        objects = list() if objects is None else list(objects)
        objects.append(AMain_item['object'])
        data['element']['items'] = objects

    return data

def get_data(data = None):
    return data if data is not None else {
            'element': {
                'fields': None,
                'items': None
            },
            'need_category': True
        }