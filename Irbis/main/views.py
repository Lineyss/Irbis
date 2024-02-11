from .session_filters import apply_filters, apply_page, is_empty
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models_fields import *
from .not_urls_views import *
from django.forms import *
from .models import *
from .forms import *

DEFAULT_SEARCH_AREA = 'Везде'
ITEMS_PER_PAGE = 10

def index(request):
    return render(request, 'main/index.html', request.forms_data)

def by_category(request, name, search:str=None):    
    category_obj = Category.objects.get(name=name)
    page_num = 1 if is_empty(request.GET.get('page_num')) else int(request.GET.get('page_num'))

    if search:
        search_result = search_items(search, category_obj)
        items = apply_filters(request, search_result['found_items'])

        paginator = Paginator(items, ITEMS_PER_PAGE)
        page_object = apply_page(paginator, page_num)
        page_object.adjusted_elided_pages = paginator.get_elided_page_range(page_num)

        data = {
            'category': name,
            'items': page_object.object_list,
            'fields': search_result['fields'],
            'is_compose': search_result['is_compose'],
            'model': search_result['model'],
            'page_obj': page_object,
        }
        
        data = data | request.forms_data

        return render(request, 'main/category_items.html', data)
        
    furnitures = get_furnitures(category_obj)
    items = apply_filters(request, furnitures['items'])

    paginator = Paginator(items, ITEMS_PER_PAGE)
    page_object = apply_page(paginator, page_num)
    page_object.adjusted_elided_pages = paginator.get_elided_page_range(page_num)
        
    data = {
        'category': name,
        'items': page_object.object_list,
        'fields': furnitures['fields'],
        'is_compose': furnitures['is_compose'],
        'model': furnitures['model'],
        'page_obj': page_object,
    }
        
    data = data | request.forms_data

    return render(request, 'main/category_items.html', data)

def composition(request, model_name:str, composed_id:int):
    page_num = 1 if is_empty(request.GET.get('page_num')) else int(request.GET.get('page_num'))

    model = apps.get_model('main', model_name)
    model_item = model.objects.get(pk=composed_id)

    compose_model = apps.get_model('main', model_name+"Composition")
    comps = get_compositions(model_name, composed_id)

    fields = get_model_not_auto_created_fields(compose_model)
    fields = reorder_compose_fields(fields)
    composed_field_name = fields[0].attname

    related_model = compose_model._meta.get_field(composed_field_name[:len(composed_field_name)-3:]).related_model

    paginator = Paginator(comps, ITEMS_PER_PAGE)
    page_object = apply_page(paginator, page_num)
    page_object.adjusted_elided_pages = paginator.get_elided_page_range(page_num)

    data = {
        'model': composed_field_name[:len(composed_field_name)-3:],
        'item': model_item,
        'comps': page_object.object_list,
        'fields': fields,
        'composed_field': composed_field_name,
        'page_obj': page_object,

        'is_compose': is_composable(related_model)
    }
        
    data = data | request.forms_data

    return render(request, 'main/composition.html', data)

def search(request):
    search = request.POST.get('search')
    search_area = request.POST.get('search_area')
    
    request.session['search'] = search
    request.session['search_area'] = search_area

    if search == '' or search is None:
        return redirect('main_index')

    request.forms_data['search'] = search
    request.forms_data['search_area'] = search_area

    found_items = []

    if search_area != DEFAULT_SEARCH_AREA:
        return redirect('by_category', name=search_area, search=search)
    else:
        search_result = search_items(search)
        found_items = search_result['found_items']

        grouped_items = group_list_by_category(found_items)
        
        data = {
            'grouped_items': grouped_items,
        }
        
        data = data | request.forms_data

    return render(request, 'main/search.html', data)

def detail_view(request,name,pk):

    category = Category.objects.get(name = name)
    model = get_furnitures(category)['model']
    model = model.objects.get(pk = pk)

    data = {}

    if model._meta.verbose_name == 'Модуль':
        data = module_detail_view(model)
    elif model._meta.verbose_name == 'PCB':
        data = pcb_detail_view(model)
    else:
        return redirect('update_view', name , pk)
    
    data['detailView'] = True

    return render(request, 'main/category_view.html', data)

def update_view(request, name,pk):
    category = Category.objects.get(name = name)
    model = get_furnitures(category)['model']
    model = model.objects.get(pk = pk)
    
    form = get_model_form(model)

    if request.method == 'GET':
        
        data = {
            'form': form(instance=model),
            'title': model._meta.verbose_name
        }
        
        return render(request, 'main/category_view.html', data)
    
    elif request.method == 'POST':
        form = form(request.POST, request.FILES, instance=model)
        if form.is_valid():
            form.save()

        return redirect('update_view', name , pk)

def create_category(request, name):
    print(name)
    category = Category.objects.get(name = name)
    model = get_furnitures(category)['model']

    createView = get_createViewModel(model)

    return createView(request)

# Не используемые view в url