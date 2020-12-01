import json
from levelupapi.models.gamer import Gamer
from levelupapi.models.game import Game
from rest_framework import status
from rest_framework.test import APITestCase
from levelupapi.models import Event, GameType

class EventTests(APITestCase):
    def setUp(self):
        """
        Create a new account and create sample category
        """
        url = "/register"
        data = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com",
            "address": "100 Infinity Way",
            "phone_number": "555-1212",
            "first_name": "Steve",
            "last_name": "Brownlee",
            "bio": "Love those gamez!!"
        }
        # Initiate request and capture response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Store the auth token
        self.token = json_response["token"]

        # Assert that a user was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # SEED DATABASE WITH ONE GAME TYPE
        # This is needed because the API does not expose a /gametypes
        # endpoint for creating game types
        gametype = GameType()
        gametype.label = "Board game"
        gametype.save()


        game = Game()
        game.id = 1
        game.gamer_id = 1
        game.number_of_players = 1
        game.skill_level = 1
        game.title = "foo"
        game.gametype_id = 1
        game.save()

    def test_create_event(self):
        """
        Ensure we can create a new event.
        """
        # DEFINE GAME PROPERTIES
        url = "/events"
        data = {
            "gamer_id": 1,
            "date": "2021-10-04",
            "time": "12:00:00",
            "gameId": 1,
            "description": "foo"
        }

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["gamer"]["user"]["first_name"], "Steve")
        self.assertEqual(json_response["date"], "2021-10-04")
        self.assertEqual(json_response["time"], "12:00:00")
        self.assertEqual(json_response["game"]["id"], 1)
        self.assertEqual(json_response["id"], 1)


    def test_get_event(self):
        """
        Ensure we can get an existing event.
        """

        # Seed the database with an event
        event = Event()
        event.gamer_id = 1
        event.date = "2020-11-30"
        event.time = "12:00:00"
        event.location = "Nashville"
        event.game_id = 1

        event.save()

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.get(f"/events/{event.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["id"], 1)
        self.assertEqual(json_response["date"], "2020-11-30")
        self.assertEqual(json_response["time"], "12:00:00")


    def test_change_event(self):
        """
        Ensure we can change an existing event.
        """


        # Seed the database with an event
        event = Event()
        event.gamer_id = 1
        event.date = "2020-11-30"
        event.time = "12:00:00"
        event.description = "Nashville"
        event.game_id = 1

        event.save()

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "gamer_id": 2,
            "date": "2020-12-01",
            "time": "11:59:00",
            "description": "Atlanta",
            "gameId": 1
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(f"/events/{event.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET GAME AGAIN TO VERIFY CHANGES
        response = self.client.get(f"/events/{event.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the properties are correct
        self.assertEqual(json_response["date"], "2020-12-01")
        self.assertEqual(json_response["time"], "11:59:00")

    def test_delete_event(self):
        """
        Ensure we can delete an existing event.
        """
        # Seed the database with an event
        event = Event()
        event.gamer_id = 1
        event.date = "2020-11-30"
        event.time = "12:00:00"
        event.description = "Nashville"
        event.game_id = 1

        event.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(f"/events/{event.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET GAME AGAIN TO VERIFY 404 response
        response = self.client.get(f"/events/{event.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)