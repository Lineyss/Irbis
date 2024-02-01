from django.core.paginator import Paginator, EmptyPage

def check_filters(request):
    apply = False if request.POST.get('apply') is None else True
    cancel = False if request.POST.get('cancel') is None else True
    
    if apply:
        confirm_filters(request)
    elif cancel:
        clear_filters(request)

def confirm_filters(request):
    min = request.POST.get('min')
    max = request.POST.get('max')
    place = request.POST.get('place')

    if min is not None:
        request.session['min'] = min
    if max is not None:
        request.session['max'] = max
    if place is not None:
        request.session['place'] = place

def clear_filters(request):
    request.session['min'] = None
    request.session['max'] = None
    request.session['place'] = None

def apply_filters(request, items: list) -> list:
    min = request.session.get('min')
    max = request.session.get('max')
    place = request.session.get('place')

    if not is_empty(place):
        place = str(place)
        items = list(filter(lambda item: str.__contains__(str(getattr(item, 'place')).lower(), place.lower()), items))
    if not is_empty(min):
        min = int(min)
        items = list(filter(lambda item: getattr(item, 'quantity') >= min, items))
    if not is_empty(max):
        max = int(max)
        items = list(filter(lambda item: getattr(item, 'quantity') <= max, items))

    return items

def apply_page(paginator: Paginator, page_num: int):
    try:
        page_object = paginator.page(page_num)
    except EmptyPage:
        page_object = paginator.page(1)

    return page_object

def is_empty(value):
    return value is None or value == ''