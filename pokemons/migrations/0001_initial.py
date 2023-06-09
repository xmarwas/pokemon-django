# Generated by Django 4.2.1 on 2023-06-01 14:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Pokemon",
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
                ("name", models.CharField(max_length=255, unique=True)),
                (
                    "order",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(0)]
                    ),
                ),
                (
                    "height",
                    models.FloatField(
                        validators=[django.core.validators.MinValueValidator(0)]
                    ),
                ),
                (
                    "weight",
                    models.FloatField(
                        validators=[django.core.validators.MinValueValidator(0)]
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PokemonType",
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
                ("type", models.CharField(max_length=255, unique=True)),
                (
                    "pokemons",
                    models.ManyToManyField(related_name="types", to="pokemons.pokemon"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Move",
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
                ("name", models.CharField(max_length=255, unique=True)),
                (
                    "power",
                    models.PositiveIntegerField(
                        validators=[django.core.validators.MinValueValidator(0)]
                    ),
                ),
                (
                    "pokemons",
                    models.ManyToManyField(related_name="moves", to="pokemons.pokemon"),
                ),
            ],
        ),
    ]
