# Generated by Django 3.2.6 on 2021-08-16 20:12

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Creator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('rating', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)])),
                ('foundation_date', models.DateField(auto_now_add=True)),
                ('logo_url', models.URLField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GameCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=150)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название игры')),
                ('description', models.TextField(verbose_name='Краткое описание игры')),
                ('rating', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)], verbose_name='Рейтинг игры')),
                ('create_date', models.DateField(auto_now_add=True, verbose_name='Дата выхода игры')),
                ('logo_url', models.URLField(null=True)),
                ('categories', models.ManyToManyField(related_name='categories', to='api.GameCategory')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.creator')),
            ],
        ),
    ]
