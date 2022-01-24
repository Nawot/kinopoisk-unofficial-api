import asyncio
import unittest
import aiounittest
import kinopoisk.client
import dotenv
import os

dotenv.load_dotenv()
token = os.getenv('TOKEN')

class TestGetMovieData(aiounittest.AsyncTestCase):


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


    async def test_has_id(self):
        for i in (301, 178707, 859908, 1309570):
            response = await self.client.get_movie_data(i)

            self.assertIsNotNone(response.id)
            self.assertIsNotNone(response.id.kinopoisk)

    
    async def test_incorect_incoming_data(self):
        for i in (True, False, 'fjdalj', -439, self.client, self):
            response = await self.client.get_movie_data(i)
            self.assertIsNone(response)

