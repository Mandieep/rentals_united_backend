# Generated by Django 4.2.4 on 2023-08-17 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental_properties_app', '0011_remove_propertycheckincheckout_early_departure_fee_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='propertycharges',
            name='applied_to',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='propertycharges',
            name='extra_charge_type',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='propertycharges',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
