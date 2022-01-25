import aiohttp
import asyncio

from kinopoisk.data.fact import Fact
from kinopoisk.data.blooper import Blooper
from kinopoisk.data.box_office import BoxOffice
from kinopoisk.data.review import Review
from kinopoisk.data.person import Person
from kinopoisk.data.movie import BaseMovie, Film, TVSeries, Season, Episode
from kinopoisk.data.types import MovieTypes, FactTypes
from .errors import *


class KPClient:
    """Simple API wrapper for getting data."""

    __base_url = 'https://kinopoiskapiunofficial.tech/api/v'

    def __init__(self, token : str):
        self.__session = aiohttp.ClientSession(
            headers={'X-API-KEY': token, 'accept': 'application/json'})
    

    def __del__(self):
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(self.__session.close())
            else:
                loop.run_until_complete(self.__session.close())
        except Exception:
            pass
    

    @staticmethod
    async def __check_status_code(code : int) -> bool:
        """
        Checkes status code on some errors[].

        @param code: status code.
        @raise InvalidTokenError: If status code 401
        @raise TooManyRequestsError: If status code 429
        @return bool: If all right True else False.
        """

        if code == 401:
            raise InvalidTokenError
        if code == 429:
            raise TooManyRequestsError
        if code == 404:
            return False
        if code == 400:
            return False
        return True
    

    @staticmethod
    async def __create_movie_by_json(json : dict) -> (BaseMovie, Film, TVSeries, None):
        """
        Creates movie needed type e.g. Film or TVSiries.

        @param json: This is dict return of server.
        @return movie or None if the movie of unsupported type
        """

        movie = None
        type = None
        try:
            # Not always request have a type. The get_similars methods return without regular type but another type.
            if json.get('relationType') == 'SIMILAR':
                movie = await BaseMovie._create_from_json(json)
            else:
                type = MovieTypes(json.get('type'))
                if type is None:
                    type = MovieTypes.tv_series if json.get('serial') else MovieTypes.film
        except ValueError:
            return None
        
        if type == MovieTypes.film:
            movie = await Film._create_from_json(json)
        elif type == MovieTypes.tv_series:
            movie = await TVSeries._create_from_json(json)
        
        return movie



    async def get_movie_data(self, id) -> (Film, TVSeries, None):
        """
        Getting the data for a movie from the API and returns it as a movie object.
        
        @param id: Id of the movie that data to be fetched.
        @return: film, tv series. If some error that None.
        """

        version = '2.2'
        async with self.__session.get(f'{self.__base_url}{version}/films/{id}') as response:
            code = response.status
            if not await self.__check_status_code(code): return
            
            json = await response.json()
            movie = await KPClient.__create_movie_by_json(json)
            return movie
    

    async def get_seasons_data(self, id) -> (list[Season], None):
        """
        Gets the seasons data. It takes in an id of movie and returns the list of seasons.
        
        @param id: Movie id to get the seasons from.
        @return: The list of movie seasons. None if some error.
        """

        version = '2.2'
        async with self.__session.get(f'{self.__base_url}{version}/films/{id}/seasons') as response:
            code = response.status
            if not await self.__check_status_code(code): return
            
            json = await response.json()
            seasons = []
            items = json.get('items')
            if items is None: return
            for item in items:
                seasons.append(await Season._create_from_json(item))
            return seasons


    async def get_facts(self, id) -> (list[Fact, Blooper], None):
        """
        Gets the facts and blooper from film.
        
        @param id: Movie id.
        @return: List of Fact and Blooper, or None if the API call fails.
        """

        version = '2.2'
        async with self.__session.get(f'{self.__base_url}{version}/films/{id}/facts') as response:
            code = response.status
            if not await self.__check_status_code(code): return
            
            json = await response.json()
            facts = []
            items = json.get('items')
            if items is None: return
            for item in items: 
                if FactTypes(item.get('type')) == FactTypes.fact:
                    facts.append(await Fact._create_from_json(item))
                elif FactTypes(item.get('type')) == FactTypes.blooper:
                    facts.append(await Blooper._create_from_json(item))
            return facts
    

    async def get_box_office(self, id) -> (BoxOffice, None):
        """
        Gets the box office data by a film id.
        
        @param id: Movie id.
        @return: BoxOffice. None if some error.
        """

        version = '2.2'
        async with self.__session.get(f'{self.__base_url}{version}/films/{id}/box_office') as response:
            code = response.status
            if not await self.__check_status_code(code): return
            
            json = await response.json()
            box_office = await BoxOffice._create_from_json(json)
            return box_office
    

    async def get_sequels_and_prequels(self, id) -> (dict[Film], None):
        """
        Gets the sequels and prequels of a film.
        
        @param id: Movie id.
        @return: Dict of 'sequels' and 'prequels'. None if some error.
        """

        version = '2.1'
        async with self.__session.get(f'{self.__base_url}{version}/films/{id}/sequels_and_prequels') as response:
            code = response.status
            if not await self.__check_status_code(code): return
            
            films = {'sequels': [], 'prequels': []}
            json = await response.json()
            if json is None: return
            # If error, server returning dict with message of error.
            if isinstance(json, dict): return
            for film in json:
                if film.get('relationType') == 'SEQUEL':
                    films['sequels'].append(await Film._create_from_json(film))
                elif film.get('relationType') == 'PREQUEL':
                    films['prequels'].append(await Film._create_from_json(film))
            return films
    

    async def get_reviews(self, id, page : int=1) -> (list[Review], None):
        """
        Gets reviews of movie by it id. Also takes page number.
        
        @param id: Movie id.
        @param page: Used to specify which page of results to getting data.
        @return: List of Review objects.
        """
        
        version = '1'
        async with self.__session.get(f'{self.__base_url}{version}/reviews?filmId={id}&page={page}') as response:
            code = response.status
            if not await self.__check_status_code(code): return
            
            reviews = []
            json = await response.json()
            items = json.get('reviews')
            if items is None: return
            for review in items:
                reviews.append(await Review._create_from_json(review))
            return reviews
    

    async def get_persons_of_movie(self, id) -> (list[Person], None):
        """
        Gets the persons of a movie.
        
        @param id: Movie id.
        @return: List of Person objects that were found in the given movie.
        """

        version = '1'
        async with self.__session.get(f'{self.__base_url}{version}/staff?filmId={id}') as response:
            code = response.status
            if not await self.__check_status_code(code): return
            
            persons = []
            json = await response.json()
            if json is None: return
            for person in json:
                persons.append(await Person._create_from_json(person))
            return persons


    async def get_person_data(self, id) -> (Person, None):
        """
        Gets the data of a person by it id. Gets more info that get_persons_of_movie but already by person id.
        
        @param id: Person id.
        @return: Person with additional info. None if some error.
        """

        version = '1'
        async with self.__session.get(f'{self.__base_url}{version}/staff/{id}') as response:
            code = response.status
            if not await self.__check_status_code(code): return
            
            json = await response.json()
            person = await Person._create_from_json(json)
            return person


    async def search_person(self, name : str, page : int=None) -> (list[Person], None): 
        """
        Searches for a person by name. It takes in a name of person, and an optional page number to search through.
        
        @param name: Person name.
        @param page: Used to specify a page number.
        @return: List of persons.
        """
        version = '1'

        query = ''
        if name is not None:
            query += f'name={name}&'
        if page is not None:
            query += f'page={page}&'

        async with self.__session.get(f'{self.__base_url}{version}/persons?{query}') as response:
            code = response.status
            if not await self.__check_status_code(code): return
            
            persons = []
            json = await response.json()
            items = json.get('items')
            if items is None or items == []: return
            for person in items:
                persons.append(await Person._create_from_json(person))
            return persons


    async def search_movie(
        self,
        keyword : str=None,
        year_from : int=None,
        year_to : int=None,
        rating_from : int=None,
        rating_to : int=None,
        type : MovieTypes=None,
        page : int=None
    ) -> (Film, TVSeries, None):
        """
        Searches for a movie by keyword, year of release, rating and type.
        If the search is successful it returns a list of movies that match the criteria.
        
        @param keyword: Keyword by which you want get movie.
        @param year_from: Start year of a movie.
        @param year_to: End year of a movie.
        @param rating_from: Filter out movies with a rating lower than this value.
        @param rating_to: Filter out movies with rating less than this value.
        @param type: Type of movie. Type is a string enum named MovieTypes 
        @param page: Used to get the next page of results.
        @return: List of movies that match the given criteria. None if some errors.
        """
        version = '2.2'
        is_unsupported_type = False 
        query = ''
        if keyword is not None:
            query += f'keyword={keyword}&'
        if year_from is not None:
            query += f'yearFrom={year_from}&'
        if year_to is not None:
            query += f'yearTo={year_to}&'
        if rating_from is not None:
            query += f'ratingFrom={rating_from}&'
        if rating_to is not None:
            query += f'ratingTo={rating_to}&'
        if page is not None:
            query += f'page={page}&'
        
        if type is not None:
            if type in (MovieTypes.all, MovieTypes.film, MovieTypes.tv_show):
                query += f'type={type}&'
            else:
                is_unsupported_type = True

        async with self.__session.get(f'{self.__base_url}{version}/films?{query}') as response:
            code = response.status
            if not await self.__check_status_code(code): return
            
            items = []
            json = await response.json()
            _items = json.get('items')
            if _items is None: return
            for item in _items:
                if is_unsupported_type:
                    if MovieTypes(item['type']) == type:
                        items.append(item)
                else:
                    items.append(item)
            
            movies = []
            for item in items:
                movie = await self.__create_movie_by_json(item)
                # If movie unsupported type, returned None, so not appending this to result.
                if movie is not None: movies.append(movie)
            if movies != []:
                return movies


    async def get_similars(self, id) -> (list[Film, TVSeries], None):
        """
        Getting similars movies by movie id from the API and returns it as a movies list.
        
        @param id: Id of the movie that data to be fetched.
        @return: film, tv series. If some error that None.
        """

        version = '2.2'
        async with self.__session.get(f'{self.__base_url}{version}/films/{id}/similars') as response:
            code = response.status
            if not await self.__check_status_code(code): return
            
            movies = []
            json = await response.json()
            items = json.get('items')
            if items is None or items == []: return
            for movie in items:
                movies.append(await KPClient.__create_movie_by_json(movie))
            return movies
