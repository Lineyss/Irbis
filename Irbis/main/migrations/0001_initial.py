# Generated by Django 4.2.6 on 2023-11-16 09:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=100, unique=True, verbose_name="Название"
                    ),
                ),
            ],
            options={
                "verbose_name": "Категория",
                "verbose_name_plural": "Категории",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Element",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "quantity",
                    models.IntegerField(
                        default=0, null=True, verbose_name="Кол-во на складе"
                    ),
                ),
                ("place", models.TextField(verbose_name="Место")),
                (
                    "mfr_part_num",
                    models.CharField(
                        max_length=100,
                        unique=True,
                        verbose_name="Номер детали производителя",
                    ),
                ),
                (
                    "lcsc_part_num",
                    models.CharField(
                        max_length=100, unique=True, verbose_name="Номер детали LCSC"
                    ),
                ),
                ("comment", models.TextField(verbose_name="Описание элемента")),
                (
                    "designator",
                    models.TextField(verbose_name="Идентификатор компонента"),
                ),
                (
                    "footprint",
                    models.CharField(
                        max_length=100, verbose_name="Схема размещения площадок"
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="main.category",
                        verbose_name="Категория",
                    ),
                ),
            ],
            options={
                "verbose_name": "Элемент",
                "verbose_name_plural": "Элементы",
                "ordering": ["mfr_part_num"],
            },
        ),
        migrations.CreateModel(
            name="Employee",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="Имя")),
                ("surname", models.CharField(max_length=50, verbose_name="Фамилия")),
                (
                    "middlename",
                    models.CharField(max_length=50, null=True, verbose_name="Отчество"),
                ),
            ],
            options={
                "verbose_name": "Сотрудник",
                "verbose_name_plural": "Сотрудники",
                "ordering": ["surname"],
            },
        ),
        migrations.CreateModel(
            name="Module",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "quantity",
                    models.IntegerField(
                        default=0, null=True, verbose_name="Кол-во на складе"
                    ),
                ),
                ("place", models.TextField(verbose_name="Место")),
                ("name", models.CharField(max_length=255, verbose_name="Название")),
                (
                    "element_quantity",
                    models.IntegerField(
                        default=1, verbose_name="Необходимое количество элемента"
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="main.category",
                        verbose_name="Категория",
                    ),
                ),
                (
                    "element",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="main.element",
                        verbose_name="Элемент",
                    ),
                ),
            ],
            options={
                "verbose_name": "Модуль",
                "verbose_name_plural": "Модули",
            },
        ),
        migrations.CreateModel(
            name="PCB",
            fields=[
                (
                    "number",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="Номер п/п",
                    ),
                ),
                (
                    "quantity",
                    models.IntegerField(
                        default=0, null=True, verbose_name="Кол-во на складе"
                    ),
                ),
                ("place", models.TextField(verbose_name="Место")),
                ("name", models.CharField(max_length=255, verbose_name="Название")),
                (
                    "decimal_number",
                    models.CharField(
                        max_length=10, unique=True, verbose_name="Децимальный номер"
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="main.category",
                        verbose_name="Категория",
                    ),
                ),
                (
                    "developed_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="main.employee",
                        verbose_name="Разработал",
                    ),
                ),
                (
                    "elements",
                    models.ManyToManyField(
                        related_name="elements",
                        through="main.Module",
                        to="main.element",
                        verbose_name="Элементы",
                    ),
                ),
            ],
            options={
                "verbose_name": "Плата",
                "verbose_name_plural": "Платы",
                "ordering": ["number"],
            },
        ),
        migrations.AddField(
            model_name="module",
            name="pcb",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="main.pcb",
                verbose_name="Печатная плата",
            ),
        ),
    ]