import asyncio
import unittest
import aiounittest
import kinopoisk.client
from kinopoisk.data.movie import TVSeries, Season, Episode
import dotenv
import os

dotenv.load_dotenv()
token = os.getenv('TOKEN')

class TestGetSeasonsData(aiounittest.AsyncTestCase):


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
        for i in (178707, 859908):
            response = await self.client.get_seasons_data(i)
            self.assertIsInstance(response, list)


    async def test_is_not_none(self):
        for i in(178707, 859908):
            response = await self.client.get_seasons_data(i)
            self.assertIsNotNone(response)
            self.assertGreater(len(response), 0)
            self.assertIsNotNone(response[0])


    async def test_contain_episodes(self):
        for i in(178707, 859908):
            response = await self.client.get_seasons_data(i)
            for season in response:
                for episode in season.episodes:
                    self.assertIsInstance(episode, Episode)
    
    
    async def test_incorect_incoming_data(self):
        for i in (True, False, 'fjdalj', -439, self.client, self):
            response = await self.client.get_seasons_data(i)
            self.assertIsNone(response)


