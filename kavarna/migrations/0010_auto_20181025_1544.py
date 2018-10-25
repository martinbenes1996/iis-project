# Generated by Django 2.0.5 on 2018-10-25 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kavarna', '0009_auto_20181023_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cafe',
            name='capacity',
            field=models.PositiveSmallIntegerField(blank=True),
        ),
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
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='cafe',
            name='housenumber',
            field=models.PositiveIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='cafe',
            name='opensAt',
            field=models.TimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='cafe',
            name='psc',
            field=models.PositiveIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='cafe',
            name='street',
            field=models.CharField(blank=True, max_length=64),
        ),
    ]