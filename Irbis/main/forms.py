from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from typing import Any, Type
from django import forms
from .models import *

def get_model_form(Model:Type[models.Model]):
    """
    Метод генерации формы на основе переданной модели
    """
    class FurnitureFrom(forms.ModelForm):
        class Meta:
            model = Model
            fields = '__all__'

    return FurnitureFrom

def get_createViewModel(Model:Type[models.Model]):
    """
    Метод генерации CreateView
    """
    class FurnitureViewModel(CreateView):
        model = Model
        fields = '__all__'
        template_name = 'main/category_view.html'
        success_url = reverse_lazy('by_category')
        
        def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            data = super().get_context_data(**kwargs)
            data['title'] = Model._meta.verbose_name

            return data
            
    return FurnitureViewModel.as_view()

class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/reg.html"
    redirect_authenticated_user = True
    

# class OtherForm(ModelForm):
#     """Форма категории прочее"""
#     class Meta:
#         model = Other
#         fields = "__all__"

# class DiodesForm(ModelForm):
#     """Форма категории диоды"""
#     class Meta:
#         model = Diodes
#         fields = "__all__"

# class CapacitanceForm(ModelForm):
#     """Форма категории конденсаторы"""
#     class Meta:
#         model = Capacitors
#         fields = "__all__"

# class ResistorsForm(ModelForm):
#     """Класс категории резисторы"""
#     class Meta:
#         model = Resistors
#         fields = "__all__"

# class TransistorsForm(ModelForm):
#     """Класс категории транзисторы"""
#     class Meta:
#         model = Transistors
#         fields = "__all__"

# class PCBForm(ModelForm):
#     """Класс категории печатной платы"""
#     class Meta:
#         model = PCB
#         fields = "__all__"

# class ModuleForm(ModelForm):
#     """Класс категории элементов печатной платы"""
#     class Meta:
#         model = Module
#         fields = "__all__"