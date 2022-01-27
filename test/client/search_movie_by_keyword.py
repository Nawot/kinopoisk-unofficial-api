import asyncio
import unittest
import aiounittest
import kinopoisk.client
from kinopoisk.data.movie import Film, TVSeries
import dotenv
import os

dotenv.load_dotenv()
token = os.getenv('TOKEN')

class TestSearchMovieByKeyword(aiounittest.AsyncTestCase):


    def setUp(self):
        async def run():
            self.client = kinopoisk.client.KPClient(token)
        self.loop.run_until_complete(run())


    def tearDown(self):
        self.loop.close()


    def get_event_loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self.loop = loop
        return self.loop


    async def test_is_list(self):
        for i in ('matrix', 'supernatural', 'mr robot', 'spider man - no way home'):
            response = await self.client.search_movie_by_keyword(i)
            self.assertIsInstance(response, list)


    async def test_has_id(self):
        for i in ('matrix', 'supernatural', 'mr robot', 'spider man - no way home'):
            response = await self.client.search_movie_by_keyword(i)
            for movie in response:
                self.assertIsNotNone(movie.id)
                self.assertIsNotNone(movie.id.kinopoisk)
    
    
    async def test_incorect_incoming_data(self):
        for i in (self.client, self):
            response = await self.client.search_movie_by_keyword(i)
            self.assertIsNone(response)


