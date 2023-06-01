from django.urls import path
from .views import (
    PokemonListView,
    PokemonCreateView,
    PokemonDetailView,
    PokemonBestMoveView,
    PokemonSimilarView,
    MoveListView,
    MoveCreateView,
    MoveDetailView,
    PokemonTypeListView,
    PokemonTypeCreateView,
    PokemonTypeDetailView,
)


urlpatterns = [
    path("pokemons/", PokemonListView.as_view(), name="pokemon-list"),
    path("pokemons/create/", PokemonCreateView.as_view(), name="pokemon-create"),
    path("pokemons/<int:pk>/", PokemonDetailView.as_view(), name="pokemon-detail"),
    path(
        "pokemons/<int:pk>/best_move/",
        PokemonBestMoveView.as_view(),
        name="pokemon-best-move",
    ),
    path(
        "pokemons/<int:pk>/similar_pokemon/",
        PokemonSimilarView.as_view(),
        name="pokemon-similar",
    ),
    path("moves/", MoveListView.as_view(), name="move-list"),
    path("moves/create/", MoveCreateView.as_view(), name="move-create"),
    path("moves/<int:pk>/", MoveDetailView.as_view(), name="move-detail"),
    path("types/", PokemonTypeListView.as_view(), name="type-list"),
    path("types/create/", PokemonTypeCreateView.as_view(), name="type-create"),
    path("types/<int:pk>/", PokemonTypeDetailView.as_view(), name="type-detail"),
]
