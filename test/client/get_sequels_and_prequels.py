import asyncio
import unittest
import aiounittest
import kinopoisk.client
from kinopoisk.data.movie import Film
import dotenv
import os

dotenv.load_dotenv()
token = os.getenv('TOKEN')

class TestGetSequelsAndPrequels(aiounittest.AsyncTestCase):


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


    async def test_is_dict(self):
        for i in (301, 178707, 1309570):
            response = await self.client.get_sequels_and_prequels(i)
            self.assertIsInstance(response, dict)


    async def test_contain_film(self):
        for i in(301, 178707, 1309570):
            response = await self.client.get_sequels_and_prequels(i)
            for sequel in response.get('sequels'):
                self.assertIsInstance(sequel, Film)
            for prequel in response.get('prequels'):
                self.assertIsInstance(prequel, Film)
    
    
    async def test_incorect_incoming_data(self):
        for i in (True, False, 'fjdalj', -439, self.client, self):
            response = await self.client.get_sequels_and_prequels(i)
            self.assertIsNone(response)




