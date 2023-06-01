from django.core.validators import MinValueValidator
from django.db import models


class Pokemon(models.Model):
    name = models.CharField(max_length=255, unique=True)
    order = models.IntegerField(validators=[MinValueValidator(0)])
    height = models.FloatField(validators=[MinValueValidator(0)])
    weight = models.FloatField(validators=[MinValueValidator(0)])

    def __str__(self):
        return self.name


class PokemonType(models.Model):
    type = models.CharField(max_length=255, unique=True)
    pokemons = models.ManyToManyField(Pokemon, related_name="types")

    def __str__(self):
        return self.type


class Move(models.Model):
    name = models.CharField(max_length=255, unique=True)
    power = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    pokemons = models.ManyToManyField(Pokemon, related_name="moves")

    def __str__(self):
        return self.name
