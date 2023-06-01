import requests
import asyncio
import argparse
import json
from dataclasses import dataclass
from typing import List

BASE_URL = "http://pokeapi.co/api/v2"
LIMIT = 1


@dataclass
class Type:
    name: str


@dataclass
class Move:
    name: str
    power: int


@dataclass
class Pokemon:
    name: str
    order: int
    height: float
    weight: float
    types: List[Type]
    moves: List[Move]


async def get_json(url: str) -> dict:
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


async def fetch(endpoint: str, name: str) -> List[Pokemon]:
    url = f"{BASE_URL}/{endpoint}/{name}/"
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    pokemon_list = []

    match endpoint:
        case "type":
            pokemons_field_name = "pokemon"
        case "move":
            pokemons_field_name = "learned_by_pokemon"

    for pokemon in data.get(pokemons_field_name, []):
        types = []
        moves = []

        if LIMIT > 0 and len(pokemon_list) >= LIMIT:
            break

        match endpoint:
            case "type":
                url = pokemon["pokemon"]["url"]
            case "move":
                url = pokemon["url"]

        pokemon_resp = await get_json(url)

        for type in pokemon_resp.get("types", []):
            type_url = type["type"]["url"]
            type_resp = await get_json(type_url)

            types.append(Type(name=type_resp.get("name")))

        for move in pokemon_resp.get("moves", []):
            move_url = move["move"]["url"]
            move_resp = await get_json(move_url)

            moves.append(
                Move(
                    name=move_resp.get("name"),
                    power=move_resp.get("power"),
                )
            )

        pokemon = Pokemon(
            name=data.get("name"),
            order=data.get("order"),
            height=data.get("height"),
            weight=data.get("weight"),
            types=types,
            moves=moves,
        )

        pokemon_list.append(pokemon)

    return pokemon_list


async def get_pokemon_by_type(type_name: str) -> List[Pokemon]:
    return await fetch("type", type_name)


async def get_pokemon_by_move(move_name: str) -> List[Pokemon]:
    return await fetch("move", move_name)


@dataclass
class Arguments:
    type: str
    move: str


async def main():
    parser = argparse.ArgumentParser()
    # type and move are mutually exclusive
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--type", type=str)
    group.add_argument("--move", type=str)
    args = Arguments(**vars(parser.parse_args()))

    if args.type:
        pokemon_list = await get_pokemon_by_type(args.type)
    elif args.move:
        pokemon_list = await get_pokemon_by_move(args.move)
    else:
        raise ValueError("Invalid arguments")

    pokemon_list = [pokemon.__dict__ for pokemon in pokemon_list]
    for pokemon in pokemon_list:
        pokemon["types"] = [type.__dict__ for type in pokemon["types"]]
        pokemon["moves"] = [move.__dict__ for move in pokemon["moves"]]

    print(json.dumps(pokemon_list, indent=2))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
