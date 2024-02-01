from import_export import resources
from .models import *

class CategoryResource(resources.ModelResource):
    """Класс для импорта/экспорта таблицы Категория"""
    class Meta:
        model = Category
        skip_unchanged = True

class EmployeeResource(resources.ModelResource):
    """Класс для импорта/экспорта таблицы Сотрудник"""
    class Meta:
        model = Employee
        skip_unchanged = True

class PCBResource(resources.ModelResource):
    """Класс для импорта/экспорта таблицы Плата"""
    class Meta:
        model = PCB
        skip_unchanged = True

class ElementResource(resources.ModelResource):
    """Класс для импорта/экспорта таблицы Элемент"""
    class Meta:
        model = Element
        skip_unchanged = True

class ModuleResource(resources.ModelResource):
    """Класс для импорта/экспорта таблицы Модуль"""
    class Meta:
        model = Module
        skip_unchanged = True

class PCBCompositionResource(resources.ModelResource):
    """Класс для импорта/экспорта таблицы Состав модуля"""
    class Meta:
        model = PCBComposition
        skip_unchanged = True

class ModuleCompositionResource(resources.ModelResource):
    """Класс для импорта/экспорта таблицы Состав модуля"""
    class Meta:
        model = ModuleComposition
        skip_unchanged = True