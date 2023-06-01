from django.test import TestCase
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient
from rest_framework import status

from .models import Pokemon, Move, PokemonType


class PokemonModelTestCase(TestCase):
    def setUp(self):
        self.pokemon = Pokemon.objects.create(
            name="Charizard", order=6, height=1.7, weight=90.5
        )
        self.type = PokemonType.objects.create(type="Fire")
        self.move = Move.objects.create(name="Flamethrower", power=90)

    def test_create_pokemon(self):
        self.assertEqual(Pokemon.objects.count(), 1)
        self.assertEqual(self.pokemon.name, "Charizard")
        self.assertEqual(self.pokemon.order, 6)
        self.assertEqual(self.pokemon.height, 1.7)
        self.assertEqual(self.pokemon.weight, 90.5)

    def test_negative_height(self):
        self.pokemon.height = -1.7
        self.assertRaises(ValidationError, self.pokemon.full_clean)

    def test_negative_weight(self):
        self.pokemon.weight = -90.5
        self.assertRaises(ValidationError, self.pokemon.full_clean)

    def test_create_pokemon_type(self):
        self.assertEqual(PokemonType.objects.count(), 1)
        self.assertEqual(self.type.type, "Fire")

    def test_create_move(self):
        self.assertEqual(Move.objects.count(), 1)
        self.assertEqual(self.move.name, "Flamethrower")
        self.assertEqual(self.move.power, 90)

    def test_pokemon_type_relationship(self):
        self.pokemon.types.add(self.type)
        self.assertEqual(self.pokemon.types.count(), 1)
        self.assertEqual(self.pokemon.types.first(), self.type)

    def test_move_pokemon_relationship(self):
        self.move.pokemons.add(self.pokemon)
        self.assertEqual(self.move.pokemons.count(), 1)
        self.assertEqual(self.move.pokemons.first(), self.pokemon)


class PokemonViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.default_format = "json"

        self.type1 = PokemonType.objects.create(type="fire")
        self.move1 = Move.objects.create(name="flamethrower", power=90)
        self.move2 = Move.objects.create(name="ember", power=60)

        self.pokemon1 = Pokemon.objects.create(
            name="Charizard", order=6, height=17, weight=905
        )
        self.pokemon1.types.add(self.type1)
        self.pokemon1.moves.add(self.move1, self.move2)

        self.valid_payload = {
            "name": "Bulbasaur",
            "order": 1,
            "height": 7,
            "weight": 69,
            "types": [self.type1.id],
            "moves": [self.move1.id, self.move2.id],
        }

        self.invalid_payload = {
            "name": "",
            "order": 0,
            "height": 0,
            "weight": 0,
            "types": [],
            "moves": [],
        }

    def test_valid_create_pokemon(self):
        response = self.client.post(
            "/pokemons/create/", data=self.valid_payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_create_pokemon(self):
        response = self.client.post(
            "/pokemons/create/", data=self.invalid_payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_pokemons(self):
        response = self.client.get("/pokemons/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["name"], self.pokemon1.name)

    def test_get_valid_single_pokemon(self):
        response = self.client.get(f"/pokemons/{self.pokemon1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.pokemon1.name)
        # check if there is field moves in response
        self.assertIn("moves", response.data)
        self.assertEqual(len(response.data["moves"]), 2)
        self.assertEqual(response.data["moves"][0]["name"], self.move1.name)
        self.assertEqual(response.data["moves"][0]["power"], self.move1.power)
        self.assertEqual(response.data["moves"][1]["name"], self.move2.name)
        self.assertEqual(response.data["moves"][1]["power"], self.move2.power)

    def test_get_invalid_single_pokemon(self):
        response = self.client.get("/pokemons/9999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_valid_delete_pokemon(self):
        response = self.client.delete(f"/pokemons/{self.pokemon1.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_pokemon(self):
        response = self.client.delete("/pokemons/9999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PokemonExtraTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.default_format = "json"

        self.type1 = PokemonType.objects.create(type="fire")
        self.move1 = Move.objects.create(name="flamethrower", power=90)
        self.move2 = Move.objects.create(name="ember", power=60)
        self.move3 = Move.objects.create(name="scratch", power=40)

        self.pokemon1 = Pokemon.objects.create(
            name="Charizard", order=6, height=17, weight=905
        )
        self.pokemon1.types.add(self.type1)
        self.pokemon1.moves.add(self.move1, self.move2, self.move3)

        self.pokemon2 = Pokemon.objects.create(
            name="Arcanine", order=59, height=19, weight=1550
        )
        self.pokemon2.types.add(self.type1)
        self.pokemon2.moves.add(self.move1, self.move2)

        self.pokemon3 = Pokemon.objects.create(
            name="Charmander", order=4, height=6, weight=85
        )
        self.pokemon3.types.add(self.type1)
        self.pokemon3.moves.add(self.move1, self.move2, self.move3)

    def test_best_move(self):
        response = self.client.get(f"/pokemons/{self.pokemon1.id}/best_move/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.move1.name)
        self.assertEqual(response.data["power"], self.move1.power)

    def test_similar_pokemon(self):
        response = self.client.get(f"/pokemons/{self.pokemon1.id}/similar_pokemon/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        data = dict(response.data[0])
        self.assertCountEqual(
            [{"id": data["id"], "name": data["name"]}],
            [{"id": self.pokemon3.id, "name": self.pokemon3.name}],
        )


class MoveViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.default_format = "json"

        self.move1 = Move.objects.create(name="flamethrower", power=90)
        self.valid_payload = {"name": "ember", "power": 60}
        self.invalid_payload = {"name": "", "power": -10}

    def test_valid_create_move(self):
        response = self.client.post(
            "/moves/create/", data=self.valid_payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_create_move(self):
        response = self.client.post(
            "/moves/create/", data=self.invalid_payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_moves(self):
        response = self.client.get("/moves/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["name"], self.move1.name)


class PokemonTypeViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.default_format = "json"

        self.type1 = PokemonType.objects.create(type="fire")
        self.valid_payload = {"type": "water"}
        self.invalid_payload = {"type": ""}

    def test_valid_create_type(self):
        response = self.client.post(
            "/types/create/", data=self.valid_payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_create_type(self):
        response = self.client.post(
            "/types/create/", data=self.invalid_payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_types(self):
        response = self.client.get("/types/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["type"], self.type1.type)
