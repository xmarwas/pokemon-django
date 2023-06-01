from rest_framework import serializers
from .models import Pokemon, PokemonType, Move


class PokemonSerializer(serializers.ModelSerializer):
    moves = serializers.SerializerMethodField()

    class Meta:
        model = Pokemon
        fields = ["id", "name", "order", "height", "weight", "types", "moves"]

    def get_moves(self, obj):
        moves = obj.moves.all().order_by("id")
        return [{"name": move.name, "power": move.power} for move in moves]


class PokemonTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PokemonType
        fields = ["id", "type"]


class MoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Move
        fields = ["id", "name", "power"]
