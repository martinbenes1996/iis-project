# Generated by Django 2.0.5 on 2018-10-23 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kavarna', '0006_auto_20181023_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cafe',
            name='city',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='cafe',
            name='closesAt',
            field=models.TimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='cafe',
            name='opensAt',
            field=models.TimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='cafe',
            name='street',
            field=models.CharField(blank=True, max_length=64),
        ),
    ]