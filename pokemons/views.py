from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import filters
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Pokemon, PokemonType, Move
from .serializers import PokemonSerializer, PokemonTypeSerializer, MoveSerializer
from django.db.models import Count


class PokemonBestMoveView(APIView):
    def get(self, request, pk, format=None):
        pokemon = Pokemon.objects.filter(id=pk).first()
        if pokemon:
            best_move = pokemon.moves.order_by("-power").first()
            if best_move:
                serializer = MoveSerializer(best_move)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"detail": "No moves available for this Pokemon."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {"detail": "Pokemon not found."}, status=status.HTTP_404_NOT_FOUND
            )


class PokemonSimilarView(APIView):
    def get(self, request, pk, format=None):
        pokemon = Pokemon.objects.filter(id=pk).first()
        if pokemon:
            moves = pokemon.moves.all()
            similar_pokemons = (
                Pokemon.objects.filter(moves__in=moves)
                .exclude(id=pokemon.id)
                .annotate(common_moves=Count("moves"))
                .filter(common_moves__gte=3)
            )
            serializer = PokemonSerializer(similar_pokemons, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"detail": "Pokemon not found."}, status=status.HTTP_404_NOT_FOUND
            )


class PokemonListView(generics.ListAPIView):
    queryset = Pokemon.objects.all().order_by("id")
    serializer_class = PokemonSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["types__type", "moves__name"]
    search_fields = ["types__type", "moves__name"]


class PokemonCreateView(generics.CreateAPIView):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer


class PokemonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer


class MoveListView(generics.ListAPIView):
    queryset = Move.objects.all().order_by("id")
    serializer_class = MoveSerializer


class MoveCreateView(generics.CreateAPIView):
    queryset = Move.objects.all()
    serializer_class = MoveSerializer


class MoveDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Move.objects.all()
    serializer_class = MoveSerializer


class PokemonTypeListView(generics.ListAPIView):
    queryset = PokemonType.objects.all().order_by("id")
    serializer_class = PokemonTypeSerializer


class PokemonTypeCreateView(generics.CreateAPIView):
    queryset = PokemonType.objects.all()
    serializer_class = PokemonTypeSerializer


class PokemonTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PokemonType.objects.all()
    serializer_class = PokemonTypeSerializer
