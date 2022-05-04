from django.test import TestCase, Client
from .models import Battle


class BattleTestCase(TestCase):
    def setUp(self):

        b1 = Battle.objects.create(name="Test Battle",
                                   wiki_link="https://en.wikipedia.org/wiki/Main_Page",
                                   date="January 1940",
                                   latitude="21.94115",
                                   longitude="-150.1212")
        b2 = Battle.objects.create(name="Fake Battle",
                                   wiki_link="https://en.wikipedia.org/wiki/Battle",
                                   date="1808 BC",
                                   latitude="-55.11774",
                                   longitude="175.92188")
        b3 = Battle.objects.create(name="Problem Battle",
                                   wiki_link="https://en.wikipedia.org/wiki/France",
                                   date="1215 AD",
                                   latitude="-92.15445",
                                   longitude="18.52241")

    def test_valid_coordinates(self):
        b = Battle.objects.get(name="Test Battle")
        self.assertTrue(b.is_valid_coordinates())

    def test_invalid_coordinates(self):
        b = Battle.objects.get(name="Problem Battle")
        self.assertFalse(b.is_valid_coordinates())

    def test_add_battle_page(self):
        client = Client()
        response = client.get("/add-battle/")
        self.assertEqual(response.status_code, 200)

    def test_get_battle(self):
        client = Client()
        response = client.get("/getbattles/18.155314/-78.441854/1/")
        self.assertEqual(response.status_code, 200)

    def test_invalid_get_battle_coordinates(self):
        client = Client()
        response = client.get("/getbattles/henry/-78.441854/-10/")
        self.assertEqual(response.status_code, 404)

    def test_add_battle_post(self):
        client = Client()
        response = client.post("/add-battle/", {
            'battle_name': 'Battle of Test',
            'battle_link': 'https://en.wikipedia.org/wiki/American_Revolution',
            'battle_date': 'February 1812',
            'battle_latitude': '21.1990',
            'battle_longitude': '-178.12221',
            'user_email': 'bob@gmail.com',
        })
        self.assertEqual(response.status_code, 302)
