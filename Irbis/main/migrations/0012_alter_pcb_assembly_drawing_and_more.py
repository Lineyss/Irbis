# Generated by Django 5.0.1 on 2024-02-13 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_module_stepfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pcb',
            name='assembly_drawing',
            field=models.FileField(blank=True, null=True, upload_to='images/<django.db.models.fields.CharField>', verbose_name='Сборный чертеж'),
        ),
        migrations.AlterField(
            model_name='pcb',
            name='electrical_diagram',
            field=models.FileField(blank=True, null=True, upload_to='images/<django.db.models.fields.CharField>', verbose_name='Электрическая схема'),
        ),
        migrations.AlterField(
            model_name='pcb',
            name='list_components',
            field=models.FileField(blank=True, null=True, upload_to='images/<django.db.models.fields.CharField>', verbose_name='Перечень компонентов'),
        ),
    ]
