# Generated by Django 5.0.1 on 2024-02-09 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_pcb_assembly_drawing_pcb_electrical_diagram_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='stepFile',
            field=models.FileField(null=True, upload_to='files/Step', verbose_name='3д модель'),
        ),
    ]
