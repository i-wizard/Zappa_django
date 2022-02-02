from rest_framework.test import APITestCase
from django.urls import resolvers, reverse

from user.models import *


class TestSetup(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.get_character_url = reverse("character")
        self.get_quote_url = reverse(
            'quote', kwargs={'pk': "5cd99d4bde30eff6ebccfe9e"})
        self.add_favorite_character = reverse(
            'character', kwargs={"pk": "5cd99d4bde30eff6ebccfe9e"})
        self.add_favorite_quote = reverse('add_quote', kwargs={
                                          "pk": "5cd99d4bde30eff6ebccfe9e", "quote_id": "5cd96e05de30eff6ebcce7ee"})
        self.get_favourite_items = reverse("favorites")
        self.registration_data = {
            "username": "sunFi",
            "password": "passcode",
            "email": "sunFi@gmail.com"
        }
        self.login_data = {
            "username": "sunFi",
            "password": "passcode"
        }

        def get_logged_in_user():
            self.client.post(self.register_url, self.registration_data)
            response = self.client.post(self.login_url, self.login_data)
            return response.data['data']['access']
        self.user_token = get_logged_in_user()

    def tearDown(self):
        return super().tearDown()
