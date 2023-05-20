"""
Module for testing user register/login journeys through test cases.
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

import copy


class UserRegistrationTestCase(TestCase):

    SAMPLE_USER_DATA = {
        "username": "abc",
        "email": "abc@gmail.com",
        "password": "qwert@123",
        "password2": "qwert@123",
        "first_name": "a",
        "last_name": "b"
    }

    def setUp(self):
        self.api_client = APIClient()

    def test_user_can_register(self):
        response = self.api_client.post(
            reverse('register_user'), self.SAMPLE_USER_DATA
        )
        self.assertEqual(response.status_code, 201)

    def test_user_register_does_not_return_password_in_response(self):
        response = self.api_client.post(
            reverse('register_user'), self.SAMPLE_USER_DATA
        )
        self.assertNotIn("password", response.json())

    def test_user_cannot_register_with_missing_required_fields(self):

        TEMP_USER_DATA = copy.deepcopy(self.SAMPLE_USER_DATA)
        del TEMP_USER_DATA['username']
        response = self.api_client.post(
            reverse('register_user'), TEMP_USER_DATA
        )
        self.assertEqual(response.status_code, 400)

        TEMP_USER_DATA = copy.deepcopy(self.SAMPLE_USER_DATA)
        del TEMP_USER_DATA['password']
        response = self.api_client.post(
            reverse('register_user'), TEMP_USER_DATA
        )
        self.assertEqual(response.status_code, 400)

        TEMP_USER_DATA = copy.deepcopy(self.SAMPLE_USER_DATA)
        del TEMP_USER_DATA['password2']
        response = self.api_client.post(
            reverse('register_user'), TEMP_USER_DATA
        )
        self.assertEqual(response.status_code, 400)

        TEMP_USER_DATA = copy.deepcopy(self.SAMPLE_USER_DATA)
        del TEMP_USER_DATA['email']
        response = self.api_client.post(
            reverse('register_user'), TEMP_USER_DATA
        )
        self.assertEqual(response.status_code, 400)

        TEMP_USER_DATA = copy.deepcopy(self.SAMPLE_USER_DATA)
        del TEMP_USER_DATA['first_name']
        response = self.api_client.post(
            reverse('register_user'), TEMP_USER_DATA
        )
        self.assertEqual(response.status_code, 400)

        TEMP_USER_DATA = copy.deepcopy(self.SAMPLE_USER_DATA)
        del TEMP_USER_DATA['last_name']
        response = self.api_client.post(
            reverse('register_user'), TEMP_USER_DATA
        )
        self.assertEqual(response.status_code, 400)

    def test_already_registered_user_cannot_re_register(self):

        response = self.api_client.post(
            reverse('register_user'), self.SAMPLE_USER_DATA
        )
        self.assertEqual(response.status_code, 201)

        # re-registering a user again.
        response1 = self.api_client.post(
            reverse('register_user'), self.SAMPLE_USER_DATA
        )
        self.assertEqual(response1.status_code, 400)
        self.assertEqual(
            response1.json()['username'], ["This field must be unique."]
        )
        self.assertEqual(
            response1.json()['email'], ["This field must be unique."]
        )

    def test_on_user_registration_watch_list_must_be_empty_symbols(self):
        response = self.api_client.post(
            reverse('register_user'), self.SAMPLE_USER_DATA
        )
        self.assertEqual(response.status_code, 201)
        user_object = User.objects.get(
            username=self.SAMPLE_USER_DATA['username']
        )
        self.assertEqual([], user_object.watchlist.symbols)

    def test_user_cannot_login_with_mismatching_passwords(self):
        TEMP_USER_DATA = copy.deepcopy(self.SAMPLE_USER_DATA)
        TEMP_USER_DATA['password2'] = "blahblahblah"
        response = self.api_client.post(
            reverse('register_user'), TEMP_USER_DATA
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            ["Password fields didn't match."], response.json()['password']
        )


class UserLoginTestCase(TestCase):

    SAMPLE_USER_DATA = {
        "username": "abc",
        "email": "abc@gmail.com",
        "password": "qwert@123",
        "password2": "qwert@123",
        "first_name": "a",
        "last_name": "b"
    }

    def setUp(self):
        self.api_client = APIClient()
        self.user = self.api_client.post(
            reverse('register_user'), self.SAMPLE_USER_DATA
        )

    def test_user_can_login(self):
        response = self.api_client.post(
            reverse('login_user'),
            {
                "username": "abc",
                "password": 'qwert@123'
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_login_response_include_token(self):
        response = self.api_client.post(
            reverse('login_user'),
            {
                "username": "abc",
                "password": 'qwert@123'
            }
        )
        self.assertIn("token", response.json())

    def test_logged_in_user_token_matches_with_db_value(self):
        response = self.api_client.post(
            reverse('login_user'),
            {
                "username": "abc",
                "password": 'qwert@123'
            }
        )
        self.assertIn("token", response.json())
        token = Token.objects.get(user__username="abc")
        self.assertEqual(token.key, response.json()['token'])

    def test_login_response_include_user_info(self):
        response = self.api_client.post(
            reverse('login_user'),
            {
                "username": "abc",
                "password": 'qwert@123'
            }
        )
        self.assertIn("user_name", response.json())
        self.assertIn("user_email", response.json())
        self.assertIn("first_name", response.json())
        self.assertIn("last_name", response.json())

    def test_on_login_user_must_get_last_saved_watch_list_symbols(self):
        # Initially watch_list is empty.
        response = self.api_client.post(
            reverse('login_user'),
            {
                "username": "abc",
                "password": 'qwert@123'
            }
        )
        self.assertEqual([], response.json()['watch_list_symbols'])

        # Mocking the behavior that user changed its watch_list symbols.
        user_object = User.objects.get(
            username=self.SAMPLE_USER_DATA['username']
        )
        user_object.watchlist.symbols = ['MSFT']
        user_object.save()

        # Login again to check if user gets MSFT.
        response = self.api_client.post(
            reverse('login_user'),
            {
                "username": "abc",
                "password": 'qwert@123'
            }
        )
        self.assertEqual(['MSFT'], response.json()['watch_list_symbols'])

    def test_login_response_must_not_contain_password(self):
        response = self.api_client.post(
            reverse('login_user'),
            {
                "username": "abc",
                "password": 'qwert@123'
            }
        )
        self.assertNotIn("password", response.json())

    def test_user_cannot_login_with_wrong_info(self):
        # user trying to logging using wrong password.
        response = self.api_client.post(
            reverse('login_user'),
            {
                "username": "abc",
                "password": 'aaaaaaaaaaaa'
            }
        )
        self.assertEqual(response.status_code, 400)

        # user trying to logging using wrong username.
        response = self.api_client.post(
            reverse('login_user'),
            {
                "username": "test_wrong_username",
                "password": 'qwert@123'
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_missing_password_or_username_throws_error(self):
        # Missing username.
        response = self.api_client.post(
            reverse('login_user'),
            {
                "password": 'qwert@123'
            }
        )
        self.assertEqual(response.status_code, 400)

        # Missing password.
        response = self.api_client.post(
            reverse('login_user'),
            {
                "username": "test_wrong_username"
            }
        )
        self.assertEqual(response.status_code, 400)
