from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    """Класс для изменения панели администратора для таблицы Категория"""
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)

@admin.register(UniqueComponent)
class UniqueComponentAdmin(ImportExportModelAdmin):
    """Клас для просмотра уникальных идентификаторов комопннетов"""
    list_display_links = None
    list_display = ('pk',)
    search_fields = ('pk',)

@admin.register(Employee)
class EmployeeAdmin(ImportExportModelAdmin):
    """Класс для изменения панели администратора для таблицы Сотрудник"""
    search_fields = ('name', 'surname', 'middlename')

class PCB_Inline(admin.TabularInline):
    model = PCBComposition
    extra = 1

class Module_Inline(admin.TabularInline):
    model = ModuleComposition
    extra = 1
    exclude = ('category',)

@admin.register(PCB)
class PCBAdmin(ImportExportModelAdmin):
    """Класс для изменения панели администратора для таблицы Плата"""
    list_display = ('number', 'name', 'decimal_number', 'PCS', 'developed_by')
    list_display_links = ('number', 'name', 'decimal_number')
    list_editable = ('PCS', 'developed_by')  
    list_filter = ('PCS', 'category', 'developed_by') 
    search_fields = ('number', 'name', 'PCS', 'category')
    exclude = ('category',)
    inlines = (PCB_Inline, Module_Inline)

    # def Элементы(self,obj):
    #     """Функция получения списка элементов платы"""
    #     return [element.mfr_part_num for element in obj.elements.all()]

@admin.register(Diodes)
class DiodesAdmin(ImportExportModelAdmin):
    """Класс для изменения панели администратора для таблицы Элемент"""
    list_display = ('ID_COMPONENT', 'MFR_PART_NUM', 'PCS', 'category' ,'BOX', 'Manufacturer')
    list_display_links = ('ID_COMPONENT', 'MFR_PART_NUM')
    list_editable = ('PCS',)
    list_filter = ('Manufacturer', 'PCS', 'ID_COMPONENT', 'MFR_PART_NUM')
    search_fields = ('ID_COMPONENT', 'MFR_PART_NUM', 'Description', 'MFR_PART_NUM', 'PCS')

@admin.register(Other)
class OtherAdmin(ImportExportModelAdmin):
    """Класс для изменения панели администатора для таблиц Другие"""
    list_display = ('ID_COMPONENT', 'MFR_PART_NUM', 'PCS', 'category' ,'BOX')
    list_display_links = ('ID_COMPONENT', 'MFR_PART_NUM')
    list_editable = ('PCS',)
    list_filter = ('PCS', 'ID_COMPONENT', 'MFR_PART_NUM')
    search_fields = ('ID_COMPONENT', 'MFR_PART_NUM', 'Description', 'MFR_PART_NUM', 'PCS')

@admin.register(Capacitors)
class CapacitorsAdmin(ImportExportModelAdmin):
    """Класс для изменения панели администратора для таблиц Конденсаторы"""
    list_display = ('ID_COMPONENT', 'MFR_PART_NUM', 'PCS', 'category' ,'BOX','Voltage_Rated','Equivalent_Series_Resistance', 'Tolerance', 'Capacitance', 'Temperature_Coefficient')
    list_display_links = ('ID_COMPONENT', 'MFR_PART_NUM')
    list_editable = ('PCS',)
    list_filter = ('PCS', 'ID_COMPONENT', 'MFR_PART_NUM')
    search_fields = ('ID_COMPONENT', 'MFR_PART_NUM', 'Description', 'MFR_PART_NUM', 'PCS')

@admin.register(Resistors)
class ResistorsAdmin(ImportExportModelAdmin):
    """Класс для изменения панели администратора для таблиц Резисторы"""
    list_display = ('ID_COMPONENT', 'MFR_PART_NUM', 'PCS', 'category' ,'BOX', 'Resistance', 'Power','Type', 'Tolerance')
    list_display_links = ('ID_COMPONENT', 'MFR_PART_NUM')
    list_editable = ('PCS',)
    list_filter = ('PCS', 'ID_COMPONENT', 'MFR_PART_NUM')
    search_fields = ('ID_COMPONENT', 'MFR_PART_NUM', 'Description', 'MFR_PART_NUM', 'PCS')

@admin.register(Transistors)
class TransistorsAdmin(ImportExportModelAdmin):
    """Класс для изменения панели администратора для таблиц Транзисторы"""
    list_display = ('ID_COMPONENT', 'MFR_PART_NUM', 'PCS', 'category' ,'BOX', 'Transition_Frequency', 'Operating_Temperature', 'Transistor_Type', 'Collector_Cut_Off_Current', 'DC_Current_Gain', 'Collector_Current', 'Power_Dissipation', 'Collector_Emitter_Saturation_Voltage', 'Collector_Emitter_Breakdown_Voltage')
    list_display_links = ('ID_COMPONENT', 'MFR_PART_NUM')
    list_editable = ('PCS',)
    list_filter = ('PCS', 'ID_COMPONENT', 'MFR_PART_NUM')
    search_fields = ('ID_COMPONENT', 'MFR_PART_NUM', 'Description', 'MFR_PART_NUM', 'PCS')

@admin.register(Module)
class ModuleAdmin(ImportExportModelAdmin):
    """Класс для изменения панели администратора для таблицы Модуль"""
    list_display = ('name', 'PCS')
    list_filter = ('PCS',)
    list_editable = ('PCS',)
    search_fields = ('name', 'PCS')
    exclude = ('category',)
    inlines = (Module_Inline,)

@admin.register(Gerber)
class GerberAdmin(ImportExportModelAdmin):
    """Класс для изменения панели админа для таблицы Гербер"""
    pass

@admin.register(PCBComposition)
class PCBCompositionAdmin(ImportExportModelAdmin):
    """Класс для изменения панели администратора для таблицы Состав модуля"""
    list_display = ('get_pcb_name', 'element', 'need_quantity')
    list_filter = ('element', 'need_quantity')
    list_editable = ('need_quantity',)
    search_fields = ('element', 'need_quantity')

    def get_pcb_name(self,obj):
        """Функция получения названия модуля"""
        return obj.pcb.name if obj.pcb else ''
    get_pcb_name.short_description = 'Плата'

@admin.register(ModuleComposition)
class ModuleCompositionAdmin(ImportExportModelAdmin):
    """Класс для изменения панели администратора для таблицы Состав модуля"""
    # list_display = ('get_module_name', 'pcb', 'element', 'element_quantity')
    list_display = ('get_module_name', 'pcb', 'need_quantity')
    list_filter = ('pcb', 'need_quantity')
    list_editable = ('need_quantity',)
    search_fields = ('pcb', 'need_quantity')

    def get_module_name(self,obj):
        """Функция получения названия модуля"""
        return obj.module.name if obj.module else ''
    get_module_name.short_description = 'Модуль'


# Admin user:
# Login: admin
# Password: admin