# Generated by Django 4.2.4 on 2023-08-19 06:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rental_properties_app', '0016_compositionroooms'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='compositionroooms',
            table='property_composition_rooms',
        ),
    ]
