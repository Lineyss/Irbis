from collections.abc import Iterable
from typing import Any
from django.db import models
import uuid

class Category(models.Model):
    """Класс категории оборудования"""

    name = models.CharField(max_length=100, unique=True, null=False, verbose_name='Название')
    """Уникальное название категории оборудования"""

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

class UniqueComponent(models.Model):
    """Класс для хранения уникальных идентификаторов компонентов"""
    def __str__(self) -> str:
        return str(self.pk)

    class Meta:
        verbose_name = 'Уникальный идентификатор комонентов'
        verbose_name_plural = 'Уникальный идентификатор комонентов'


class Compose(models.Model):
    need_quantity = models.IntegerField(default=1, verbose_name='Необходимое количество')
    """Необходимое количество"""

    class Meta:
        abstract = True

class Employee(models.Model):
    """Класс сотрудника"""

    name = models.CharField(max_length=50, null=False, verbose_name='Имя')
    """Имя"""

    surname = models.CharField(max_length=50, null=False, verbose_name='Фамилия')
    """Фамилия"""
    
    middlename = models.CharField(max_length=50, null=True, verbose_name='Отчество')
    """Отчество (может быть пустым)"""

    def __str__(self) -> str:
        return f"{self.surname} {self.name[:1]}.{self.middlename[:1]+'.' if self.middlename else ''}"

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        ordering = ['surname']

class Furniture(models.Model):
    """Базовый класс оборудования на складе"""

    PCS = models.IntegerField(default=0, null=True, verbose_name='Кол-во на складе')
    """Кол-во на складе"""

    category = models.ForeignKey(Category, null=True, editable= False ,on_delete=models.SET_NULL, verbose_name='Категория')
    """Ссылка на категорию оборудования"""

    BOX = models.TextField(null=False, verbose_name='Место')
    """Место, где находится оборудование"""

    def save(self, *args, **kwargs) -> None:

        try:
            cat = Category.objects.get(name=self._meta.verbose_name_plural)
            self.category = cat
        except:
            cat = Category.objects.create(name=self._meta.verbose_name_plural)
            self.category = cat
        
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True 

class AMain(Furniture):
    """Базовый класс для категорий Диодов, Транзисторов, Прочего, Конденсаторов, Резисторов"""

    ID_COMPONENT = models.OneToOneField(UniqueComponent, unique = True,  blank=True, editable = False, on_delete=models.CASCADE, verbose_name='Идентификатор компонента')
    """Уникальный идентификатор всех компонентов"""
    
    MFR_PART_NUM = models.CharField(max_length=100, null=True, verbose_name='Номер производителя', unique=True)
    """Уникальный номер производителя компонента"""

    Description = models.TextField(null=True, editable = False, verbose_name='Описание')
    """Описание"""

    def save(self, *args, **kwargs) -> None:
        if self.ID_COMPONENT_id is None or self.ID_COMPONENT is None:
            un = UniqueComponent.objects.create()
            self.ID_COMPONENT = un

        return super().save(*args, **kwargs)
    
    def delete(self, using: Any = ..., keep_parents: bool = ...) -> tuple[int, dict[str, int]]:
        UniqueComponent.objects.delete(pk = self.ID_COMPONENT)
        return super().delete(using, keep_parents)

    class Meta:
        abstract = True

class Other(AMain):
    """Категория прочее"""
    
    Description = models.TextField(null=True, verbose_name='Описание')
    """Описание"""

    def __str__(self) -> str:
        return f"{self.ID_COMPONENT} - {self.MFR_PART_NUM}"
    
    class Meta:
        verbose_name = 'Прочее'
        verbose_name_plural = 'Прочее'

class Element(AMain):
    """Базовый класс элементов печатной платы"""

    Photo = models.ImageField(upload_to='images/', verbose_name='Фотография')
    """Фотография компонента"""

    Manufacturer = models.CharField(max_length=100, null=False, verbose_name='Производитель')
    """Компания изготовитель компонента"""

    Package = models.CharField(max_length=100, null=False, verbose_name='Корпус компонента')
    """Корпус компонента"""
    
    def save(self, *args, **kwargs) -> None:
        self.Description = f'{self.Manufacturer} - {self.Package}'
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True

class Diodes(Element):
    """Класс диодов"""

    Forward_Voltage =models.DecimalField(max_digits=7, decimal_places=3, verbose_name = 'Прямое напряжение (Vf@If)')
    """Прямое напряжение диодов (Vf@If)"""
    
    Reverse_Voltage = models.DecimalField(max_digits=7, decimal_places=3, verbose_name = 'Обратное напряжение диода (Vr)')
    """Обратное напряжение диода (Vr)"""

    Reverse_Recovery_Time =  models.DecimalField(max_digits=7, decimal_places=3, verbose_name='Время восстановления диода (trr)')
    """Время восстановления диода"""

    Average_Rectified_Current =  models.DecimalField(max_digits=7, decimal_places=3, verbose_name='Ток (Io)')
    """Ток"""

    Diode_Configuration = models.CharField(max_length=100, verbose_name='Конфигурация сборки')
    """Конфигурация сборки"""

    Reverse_Leakage_Current = models.DecimalField(max_digits=7, decimal_places=3, verbose_name='Обратный ток утечки (Ir)')
    """Обратный ток утечки"""

    def __str__(self) -> str:
        return f"{self.ID_COMPONENT} - {self.MFR_PART_NUM}"
    
    class Meta:
        verbose_name = 'Диод'
        verbose_name_plural = 'Диоды'

class Capacitors(Element):
    """Класс конденсаторы"""

    Voltage_Rated = models.DecimalField(max_digits=6, decimal_places=3, verbose_name='Максимальное рабочее напряжение')
    """Максимальное рабочее напряжение"""

    Equivalent_Series_Resistance = models.CharField(max_length=15, verbose_name='Эквивалентное последовательное сопротивление')
    """Эквивалентное последовательное сопротивление"""

    Tolerance = models.CharField(max_length=12, verbose_name='Точность изготовления')
    """Точность изготовления"""

    Capacitance = models.DecimalField(max_digits=6, decimal_places=3, verbose_name='Емкость')
    """Емкость"""

    Temperature_Coefficient = models.CharField(max_length=10, verbose_name='Температурный коэффециент')
    """Температурный коэффециент"""
    
    def __str__(self) -> str:
        return f"{self.ID_COMPONENT} - {self.MFR_PART_NUM}"

    class Meta:
        verbose_name = 'Конденсатор'
        verbose_name_plural = 'Конденсаторы'

class Resistors(Element):
    """Класс резисторы"""
    
    Resistance = models.DecimalField(max_digits=6, decimal_places=4, verbose_name='Сопративление')
    """Сопративление"""

    Power = models.DecimalField(max_digits=6, decimal_places=4, verbose_name='Мощность')
    """Мощность"""

    Type = models.CharField(max_length=50, verbose_name='Тип')
    """Типы"""

    Tolerance = models.DecimalField(max_digits=6, decimal_places=4, verbose_name='Точность изготовления')
    """Точность изготовления"""

    def __str__(self) -> str:
        return f"{self.ID_COMPONENT} - {self.MFR_PART_NUM}"

    class Meta:
        verbose_name = 'Резистор'
        verbose_name_plural = 'Резисторы'

class Transistors(Element):
    """Класс транзисторы"""

    Transition_Frequency = models.DecimalField(max_digits=6, decimal_places=3, verbose_name='Частота перехода')
    """Частота перехода"""

    Operating_Temperature = models.CharField(max_length=12, verbose_name='Рабочая температура')
    """Рабочая температура"""
    
    Transistor_Type = models.CharField(max_length=50, verbose_name='Тип транзистора')
    """Тип транзистора"""
    
    Collector_Cut_Off_Current = models.IntegerField(verbose_name='Ток отключения коллектора')
    """Ток отключения коллектора"""
    
    DC_Current_Gain = models.CharField(max_length=12, verbose_name='Усиление постоянного тока')
    """Усиление постоянного тока"""
    
    Collector_Current = models.DecimalField(max_digits=5, decimal_places=4, verbose_name='Ток коллектора')
    """Ток коллектора"""
    
    Power_Dissipation = models.DecimalField(max_digits=5, decimal_places=4, verbose_name='Рассеиваемая мощность')
    """Рассеиваемая мощность"""
    
    Collector_Emitter_Saturation_Voltage = models.CharField(max_length=50, verbose_name='Напряжение насыщения между коллектором и  эмиттером')
    """Напряжение насыщения между коллектором и  эмиттером"""
    
    Collector_Emitter_Breakdown_Voltage = models.DecimalField(max_digits=5, decimal_places=4, verbose_name='Напряжение коллектора-эмиттера')
    """Напряжение коллектора-эмиттера"""

    def __str__(self) -> str:
        return f"{self.ID_COMPONENT} - {self.MFR_PART_NUM}"

    class Meta:
        verbose_name = 'Транзистор'
        verbose_name_plural = 'Транзисторы'

class Gerber(models.Model):
    """Класс гербер файлов"""

    file = models.FileField(upload_to='files/gerber', null=True, blank=True, verbose_name='Файл')
    """Гербер файл"""

    def __str__(self) -> str:
         return self.file.name
    
    class Meta:
        verbose_name = 'Гербер файл'
        verbose_name_plural = 'Гербер файлы'

class PCB(Furniture):
    """Класс печатной платы"""

    number = models.AutoField(primary_key=True, auto_created=True, verbose_name='Номер п/п')
    """Номер п/п"""

    name = models.CharField(max_length=255, null=False, verbose_name='Название')
    """Название"""

    decimal_number = models.CharField(max_length=10, null=False, unique=True, verbose_name='Децимальный номер')
    """Децимальный номер"""

    developed_by = models.ForeignKey(Employee, null=False, on_delete=models.PROTECT, verbose_name='Разработал')
    """Кем разработана плата"""

    list_components = models.FileField(upload_to='files/xlsx', null=True, blank=True, verbose_name='Перечень компонентов')
    """Перечень компонентов"""

    electrical_diagram = models.FileField(upload_to='files/pdf', null=True, blank=True, verbose_name='Электрическая схема')
    """Электрическая схема"""

    assembly_drawing = models.FileField(upload_to='files/pdf', null=True, blank=True, verbose_name='Сборный чертеж')
    """Сборный чертеж"""

    gerber_files = models.ManyToManyField(Gerber, null=True, blank=True, verbose_name='Гербер файлы')
    """Гербер файлы"""

    def __str__(self) -> str:
        return f"{self.decimal_number} ({self.name})"

    class Meta:
        verbose_name = "Плата"
        verbose_name_plural = "Платы"
        ordering = ['number']

class PCBComposition(Compose):
    pcb = models.ForeignKey(PCB, on_delete=models.SET_NULL, null=True, verbose_name='Печатная плата')
    """Печатная плата"""

    element = models.ForeignKey(UniqueComponent, on_delete=models.SET_NULL, null=True, verbose_name='Элемент')
    """Элемент"""

    def __str__(self):
        return f"{self.pcb} ({self.element})"

    class Meta:
        verbose_name = "Состав платы"
        verbose_name_plural = "Составы плат"

class Module(Furniture):
    """Класс состава элементов печатной платы"""

    name = models.CharField(max_length=255, null=False, unique=True, verbose_name='Название')
    """Название"""
    
    stepFile = models.FileField(null=True, upload_to='files/Step', verbose_name='3д модель')

    """3Д модель модуля """
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = "Модуль"
        verbose_name_plural = "Модули"

class ModuleComposition(Compose):
    """Класс состава модуля"""
    
    module = models.ForeignKey(Module, on_delete=models.SET_NULL, null=True, verbose_name='Модуль')
    """Модуль"""

    pcb = models.ForeignKey(PCB, on_delete=models.SET_NULL, null=True, verbose_name='Печатная плата')
    """Печатная плата"""

    def __str__(self) -> str:
        return f"{self.module} ({self.pcb})"

    class Meta:
        verbose_name = "Состав модуля"
        verbose_name_plural = "Составы модулей"


# Модели не для базы данных

class CustomField():
    """Кастомная модель столбца"""
    def __init__(self, name, verbose_name) -> None:
        """
            name - название по которому сопоставляется столбец и значение
            verbose_name - название которое будет выводиться на страницу
        """
        self.name = name 
        self.verbose_name = verbose_name
        self._verbose_name = verbose_name