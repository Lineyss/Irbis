from .models_fields import get_AMains_by_id_component
from .models import *
from .forms import *

def module_detail_view(model):
    data = {
            'module': str(model),
            'title': model._meta.verbose_name_plural,
            'file': model.stepFile,
            'pk': model.pk,
            'other': {
                'fields': '',
                'items': ()
            },
            'categoryes': {
                'fields': '',
                'items': ()
            },
            'need_category': True
        }

    moduleCompositions = ModuleComposition.objects.filter(module = model)

    for moduleComposition in moduleCompositions:

        elements = PCBComposition.objects.filter(pcb = moduleComposition.pcb)

        for element in elements:
            if(element.element is None): continue

            AMain_item = get_AMains_by_id_component(element.element.pk)

            if AMain_item['object'] is None: continue

            if AMain_item['model'] is Other:
                data['other']['fields'] = AMain_item['fields']
                objects = data['other']['items']
                objects = list(objects)
                objects.append(AMain_item['object'])
                data['other']['items'] = objects
            else:
                data['categoryes']['fields'] = AMain_item['fields']
                objects = data['categoryes']['items']
                objects = list(objects) 
                objects.append(AMain_item['object'])
                data['categoryes']['items'] = objects
    
    return data

def pcb_detail_view(model):
    data = {
        ''
    }

    return data