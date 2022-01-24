import asyncio
import unittest
import aiounittest
import kinopoisk.client
from kinopoisk.data.person import Person
import dotenv
import os

dotenv.load_dotenv()
token = os.getenv('TOKEN')

class TestGetPersonsOfMovie(aiounittest.AsyncTestCase):


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
            response = await self.client.get_persons_of_movie(i)
            self.assertIsInstance(response, list)


    async def test_contain_person(self):
        for i in(301, 178707, 1309570):
            response = await self.client.get_persons_of_movie(i)
            for person in response:
                self.assertIsInstance(person, Person)

    
    async def test_has_id(self):
        for i in(301, 178707, 1309570):
            response = await self.client.get_persons_of_movie(i)
            for person in response:
                self.assertIsNotNone(person.id)
                self.assertIsNotNone(person.id.kinopoisk)
    

    
    async def test_incorect_incoming_data(self):
        for i in (True, False, 'fjdalj', -439, self.client, self):
            response = await self.client.get_persons_of_movie(i)
            self.assertIsNone(response)





