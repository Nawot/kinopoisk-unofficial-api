import asyncio
import unittest
import aiounittest
import kinopoisk.client
from kinopoisk.data.poster import Poster
import dotenv
import os

dotenv.load_dotenv()
token = os.getenv('TOKEN')

class TestGetImages(aiounittest.AsyncTestCase):


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
        for i in (301, 178707, 1309570):
            response = await self.client.get_images(i)
            self.assertIsInstance(response, list)


    async def test_contain_poster(self):
        for i in(301, 178707, 1309570):
            response = await self.client.get_images(i)
            for poster in response:
                self.assertIsInstance(poster, Poster)
    
    
    async def test_incorect_incoming_data(self):
        for i in (True, False, 'fjdalj', -439, self.client, self):
            response = await self.client.get_images(i, i, i)
            self.assertIsNone(response)
