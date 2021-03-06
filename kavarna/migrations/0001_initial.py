# Generated by Django 2.0.5 on 2018-10-28 17:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cafe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('street', models.CharField(blank=True, max_length=64, null=True)),
                ('housenumber', models.PositiveIntegerField(blank=True, null=True)),
                ('city', models.CharField(blank=True, max_length=64, null=True)),
                ('psc', models.CharField(blank=True, max_length=64, null=True)),
                ('opensAt', models.CharField(blank=True, max_length=64, null=True)),
                ('closesAt', models.CharField(blank=True, max_length=64, null=True)),
                ('capacity', models.PositiveSmallIntegerField(blank=True, default=0, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Coffee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('place_of_origin', models.CharField(blank=True, max_length=64)),
                ('quality', models.CharField(blank=True, max_length=64)),
                ('taste_description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CoffeeBean',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('origin', models.CharField(blank=True, max_length=64)),
                ('aroma', models.CharField(blank=True, max_length=64)),
                ('acidity', models.PositiveSmallIntegerField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CoffeeContainsBeans',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percentage', models.PositiveIntegerField()),
                ('coffee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kavarna.Coffee')),
                ('coffeeBean', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kavarna.CoffeeBean')),
            ],
        ),
        migrations.CreateModel(
            name='CoffeePreparation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Drinker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.PositiveIntegerField(default='0')),
                ('fav_coffee', models.ManyToManyField(to='kavarna.Coffee')),
                ('fav_preparation', models.ManyToManyField(to='kavarna.CoffeePreparation')),
                ('likes_cafe', models.ManyToManyField(to='kavarna.Cafe')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('price', models.IntegerField()),
                ('capacity', models.IntegerField()),
                ('coffee_list', models.ManyToManyField(to='kavarna.Coffee')),
                ('participants', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kavarna.Cafe')),
            ],
        ),
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True)),
                ('date', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('score', models.PositiveSmallIntegerField(default=5)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('cafe', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='kavarna.Cafe')),
                ('event', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='kavarna.Event')),
                ('react', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='kavarna.Reaction')),
            ],
        ),
        migrations.AddField(
            model_name='coffee',
            name='beans',
            field=models.ManyToManyField(through='kavarna.CoffeeContainsBeans', to='kavarna.CoffeeBean'),
        ),
        migrations.AddField(
            model_name='coffee',
            name='preparation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='kavarna.CoffeePreparation'),
        ),
        migrations.AddField(
            model_name='cafe',
            name='offers_coffee',
            field=models.ManyToManyField(to='kavarna.Coffee'),
        ),
        migrations.AddField(
            model_name='cafe',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
