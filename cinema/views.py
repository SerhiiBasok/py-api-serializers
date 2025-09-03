from typing import Type

from django.db.models import QuerySet
from rest_framework import viewsets, serializers
from cinema.models import Genre, Actor, CinemaHall, Movie, MovieSession
from cinema.serializers import (GenreSerializer,
                                ActorSerializer,
                                CinemaHallSerializer,
                                MovieListSerializer,
                                MovieSerializer,
                                MovieSessionListSerializer,
                                MovieSessionRetrieveSerializer,
                                MovieRetrieveSerializer, MovieSessionSerializer
                                )


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ActorsViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class CinemaHallViewSet(viewsets.ModelViewSet):
    queryset = CinemaHall.objects.all()
    serializer_class = CinemaHallSerializer


class MovieViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self) -> Type[serializers.Serializer]:
        if self.action == "list":
            return MovieListSerializer
        elif self.action == "retrieve":
            return MovieRetrieveSerializer
        return MovieSerializer

    def get_queryset(self) -> QuerySet[Movie]:
        return Movie.objects.prefetch_related("genres", "actors")


class MovieSessionViewSet(viewsets.ModelViewSet):
    queryset = MovieSession.objects.all()

    def get_serializer_class(self) -> Type[serializers.Serializer]:
        if self.action == "list":
            return MovieSessionListSerializer
        elif self.action == "retrieve":
            return MovieSessionRetrieveSerializer
        return MovieSessionSerializer

    def get_queryset(self) -> QuerySet[MovieSession]:
        queryset = self.queryset
        if self.action in ("list", "retrieve"):
            return queryset.select_related(
                "movie", "cinema_hall"
            ).prefetch_related("movie__genres", "movie__actors")
        return queryset
