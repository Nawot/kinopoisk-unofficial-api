import asyncio
import kinopoisk.client

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

async def time_to_minute(str) -> int:
    """Sometime API returning movie length as str e.g. \'1:46\'. So that this function just getting minuts from it string"""
    return (x * int(t) for x, t in zip([60, 1], str.split(':')))


async def get_genre_id_by_name(name : str, is_fzf : bool=True) -> (int, None):
    """
    Search by genre name in the list of genres and returns its id.

    Before used this func you shoulde be call load_filters method of any instance KPClient else this not be to work.
    
    :param name: Name of genre
    :param is_fzf: For fuzzy search.
    :return: Id of the genre. If some error or not found - None.
    """
    if kinopoisk.client.KPClient.filters is None: return
    
    name = name.lower()

    if not is_fzf:
        for i in kinopoisk.client.KPClient.filters['genres']:
            if name == i.name.lower(): return i.id
    else:
        for i in kinopoisk.client.KPClient.filters['genres']:
            if fuzz.ratio(name, i.name.lower()) >= 85: return i.id


async def get_country_id_by_name(name : str, is_fzf : bool=True) -> (int, None):
    """
    Search by country name in the list of countries and returns its id.

    Before used this func you shoulde be call load_filters method of any instance KPClient else this not be to work.
    
    :param name: Name of country
    :param is_fzf: For fuzzy search
    :return: Id of the country. If some error or not found - None.
    """
    if kinopoisk.client.KPClient.filters is None: return

    name = name.lower()

    if not is_fzf:
        for i in kinopoisk.client.KPClient.filters['countries']:
            if name == i.name.lower(): return i.id
    else:
        for i in kinopoisk.client.KPClient.filters['countries']:
            if fuzz.ratio(name, i.name.lower()) >= 85: return i.id

