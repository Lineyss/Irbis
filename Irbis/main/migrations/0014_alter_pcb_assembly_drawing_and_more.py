# Generated by Django 5.0.1 on 2024-02-14 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_alter_pcb_assembly_drawing_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pcb',
            name='assembly_drawing',
            field=models.FileField(blank=True, null=True, upload_to='images/pdf', verbose_name='Сборный чертеж'),
        ),
        migrations.AlterField(
            model_name='pcb',
            name='electrical_diagram',
            field=models.FileField(blank=True, null=True, upload_to='images/pdf', verbose_name='Электрическая схема'),
        ),
        migrations.AlterField(
            model_name='pcb',
            name='list_components',
            field=models.FileField(blank=True, null=True, upload_to='images/xlsx', verbose_name='Перечень компонентов'),
        ),
    ]
