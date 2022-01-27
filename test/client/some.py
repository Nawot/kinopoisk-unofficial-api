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
    


class CreateMovieFromJson(aiounittest.AsyncTestCase):

    def setUp(self):
        self.client = kinopoisk.client.KPClient(token)


    def get_event_loop(self):
        self.loop = asyncio.get_event_loop()
        return self.loop


    async def test_type(self):
        response = await self.client.get_movie_data(301)
        self.assertIsInstance(response, Film)
        response = await self.client.get_movie_data(178707)
        self.assertIsInstance(response, TVSeries)
    

    async def test_incorect_incoming_data(self):
        for i in (True, False, 'fjdalj', -439, self.client, self):
            response = await self.client._KPClient__create_movie_by_json(i)
            self.assertIsNone(response)
