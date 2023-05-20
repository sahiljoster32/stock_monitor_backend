"""
Module for testing user watch_list journeys through test cases.
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

import copy


class WatchListTestCase(TestCase):

    SAMPLE_USER_DATA1 = {
        "username": "abc",
        "email": "abc@gmail.com",
        "password": "qwert@123",
        "password2": "qwert@123",
        "first_name": "a",
        "last_name": "b"
    }

    SAMPLE_USER_DATA2 = {
        "username": "test_user",
        "email": "test@gmail.com",
        "password": "abcde@123",
        "password2": "abcde@123",
        "first_name": "hi",
        "last_name": "bye"
    }

    def setUp(self):
        self.api_client = APIClient()
        self.registered_user = self.api_client.post(
            reverse('register_user'), self.SAMPLE_USER_DATA2
        )

    def test_on_first_login_watch_list_is_empty(self):
        response = self.api_client.post(
            reverse('register_user'), self.SAMPLE_USER_DATA1
        )
        self.assertEqual(response.status_code, 201)

        response = self.api_client.post(
            reverse('login_user'),
            {
                "username": "abc",
                "password": 'qwert@123'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual([], response.json()['watch_list_symbols'])

    def test_without_authentication_user_not_allowed_to_access_symbols_data_api(
        self
    ):
        response = self.api_client.post(
            reverse('fetch_symbols_data'),
            {
                'watch_list': ['MSFT']
            }
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            'Authentication credentials were not provided.',
            response.json()['detail']
        )

    def test_more_than_5_symbols_not_allowed_in_watch_list(
        self
    ):
        # Checking on logging, user gets correct token that was stored in DB.
        response = self.api_client.post(
            reverse('login_user'),
            {
                "username": "test_user",
                "password": 'abcde@123'
            }
        )
        self.assertIn("token", response.json())
        token = Token.objects.get(user__username="test_user")
        self.assertEqual(token.key, response.json()['token'])

        self.api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.api_client.post(
            reverse('fetch_symbols_data'),
            {
                'symbols': ['MSFT', 'GOOG', 'TSLA', 'APPL', 'IBM', 'XET']
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            ["Only limit of 5 symbols is allowed due to free subscription of `alpha avantage`."],
            response.json()['non_field_errors']
        )
        self.api_client.credentials()

    def test_correct_symbol_recorded_in_watch_list(self):
        response = self.api_client.post(
            reverse('login_user'),
            {
                "username": "test_user",
                "password": 'abcde@123'
            }
        )
        token = Token.objects.get(user__username="test_user")
        self.assertEqual(token.key, response.json()['token'])
        self.api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.api_client.post(
            reverse('fetch_symbols_data'),
            {
                'symbols': ['MSFT']
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(['MSFT'], response.json()['symbols'])

    def test_wrong_symbol_not_recorded_in_watch_list(self):
        response = self.api_client.post(
            reverse('login_user'),
            {
                "username": "test_user",
                "password": 'abcde@123'
            }
        )
        token = Token.objects.get(user__username="test_user")
        self.assertEqual(token.key, response.json()['token'])
        self.api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.api_client.post(
            reverse('fetch_symbols_data'),
            {
                'symbols': ['MSFT', 'BLAHBLAHBLAH']
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(['MSFT'], response.json()['symbols'])

    def test_duplicate_symbols_not_recorded_in_watch_list(self):
        response = self.api_client.post(
            reverse('login_user'),
            {
                "username": "test_user",
                "password": 'abcde@123'
            }
        )
        token = Token.objects.get(user__username="test_user")
        self.assertEqual(token.key, response.json()['token'])
        self.api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.api_client.post(
            reverse('fetch_symbols_data'),
            {
                'symbols': ['MSFT', 'MSFT']
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(['MSFT'], response.json()['symbols'])
