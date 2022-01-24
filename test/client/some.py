import asyncio
import unittest
import aiounittest
import kinopoisk.client
from kinopoisk.errors import InvalidTokenError, TooManyRequestsError
from kinopoisk.data.movie import Film, TVSeries
import dotenv
import os

dotenv.load_dotenv()
token = os.getenv('TOKEN')

class TestSome(aiounittest.AsyncTestCase):


    def setUp(self):
        self.client = kinopoisk.client.KPClient(token)


    def get_event_loop(self):
        self.loop = asyncio.get_event_loop()
        return self.loop


    async def test__check_status_code(self):
        client = kinopoisk.client.KPClient('')

        with self.assertRaises(InvalidTokenError):
            await client.get_movie_data(301) 
    

    async def test__create_movie_from_json(self):
        response = await self.client.get_movie_data(301)
        self.assertIsInstance(response, Film)
        response = await self.client.get_movie_data(178707)
        self.assertIsInstance(response, TVSeries)
