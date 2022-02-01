from rest_framework.test import APITestCase
from django.urls import resolvers, reverse

from user.models import *

class TestSetup(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.bad_username_registration_data = {
            "username":"&user$name#",
            "password":"passcode",
            "email":"user@gmail.com"
        }
        self.incomplete_registration_data = {
            "username":"&user$name#",
            "password":"passcode"
        }
        self.registration_data = {
            "username":"sunFi",
            "password":"passcode",
            "email":"sunFi@gmail.com"
        }
        self.bad_login_data={
            "username":"sunFi",
            "password":"passCode"
        }#this is prove that password is case sensitive
        self.login_data={
            "username":"sunFi",
            "password":"passcode"
        }
    def createUser():
        pass
    
    def tearDown(self):
        return super().tearDown()