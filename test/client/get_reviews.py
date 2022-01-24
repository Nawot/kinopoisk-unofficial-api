import asyncio
import unittest
import aiounittest
import kinopoisk.client
from kinopoisk.data.review import Review
import dotenv
import os

dotenv.load_dotenv()
token = os.getenv('TOKEN')

class TestGetReview(aiounittest.AsyncTestCase):


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
            response = await self.client.get_reviews(i)
            self.assertIsInstance(response, list)


    async def test_contain_review(self):
        for i in(301, 178707, 1309570):
            response = await self.client.get_reviews(i)
            for review in response:
                self.assertIsInstance(review, Review)
    
    
    async def test_incorect_incoming_data(self):
        for i in (True, False, 'fjdalj', -439, self.client, self):
            response = await self.client.get_reviews(i)
            self.assertIsNone(response)





