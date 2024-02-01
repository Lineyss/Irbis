from .models import Category
from .session_filters import check_filters


class CustomDataMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.forms_data = {}
        
        if request.method == 'POST':
            check_filters(request)

        categories = Category.objects.all().order_by('name')

        request.forms_data['categories'] = categories
        request.forms_data['min'] = request.session.get('min')
        request.forms_data['max'] = request.session.get('max')
        request.forms_data['place'] = request.session.get('place')
        request.forms_data['search'] = request.session.get('search')
        request.forms_data['search_area'] = request.session.get('search_area')
        # print(f"{request.forms_data=}")

        response = self.get_response(request)

        return response