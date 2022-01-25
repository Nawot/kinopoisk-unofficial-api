from __future__ import annotations
import asyncio
from kinopoisk.data.id import Id
from kinopoisk.data.name import Name
from kinopoisk.data.poster import Poster
from dataclasses import dataclass


@dataclass(frozen=True)
class BaseMovie:
    """Base class with general methods"""
    
    id : Id = None
    name : Name = None
    poster : Poster = None


    @staticmethod
    async def _create_from_json(json : dict) -> BaseMovie:
        movie = BaseMovie(
            id=Id(
                json.get('kinopoiskId') if json.get('kinopoiskId') is not None else json.get('filmId'),
                json.get('imdbId')),
            name=Name(original=json.get('nameOriginal'), en=json.get('nameEn'), ru=json.get('nameRu')),
            poster=Poster(json.get('posterUrl'), json.get('posterUrlPreview'))
            )
        return movie


    async def get_all_data(self, client):
        """
        Movie may not have all data, this could be that movie may be take from various API methods, which have different return data details levels.
        
        @param client: Client instance for delegating of methods.
        """

        new_ = await client.get_movie_data(self.id.kinopoisk)
        self.__dict__.update(new_.__dict__)


    async def get_reviews(self, client) -> (list[Review], None):
        """
        Gets reviews of this movie.
        
        @param client: Client instance for delegating of methods.
        """

        return await client.get_reviews(self.id.kinopoisk)
    

    async def get_persons(self, client) -> (list[Person], None):
        """
        Gets persons of this movie.
        
        @param client: Client instance for delegating of methods.
        """

        return await client.get_persons_of_movie(self.id.kinopoisk)