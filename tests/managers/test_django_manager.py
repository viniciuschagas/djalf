# -*- coding: utf-8 -*-
from mock import patch
from unittest import TestCase

from djalf.managers import TokenManagerDjango


class TestTokenManagerDjango(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.manager = TokenManagerDjango(
            'http://endpoint/token', 'client_id', 'client_secret'
        )

    @patch('djalf.managers.cache.get')
    def test_get_from_cache_should_returns_data_stored_in_cache(self, cache_get):
        self.manager._get_from_cache()

        cache_get.assert_called_once_with(self.manager._token_endpoint)

    @patch('alf.managers.TokenManager._request_token')
    @patch('djalf.managers.cache.set')
    def test_request_token_should_store_token_data_in_cache(self, cache_set, _request_token):
        token_data = {'access_token': 'access_token', 'expires_in': 10}

        _request_token.return_value = token_data

        self.manager._request_token()

        cache_set.assert_called_once_with(self.manager._token_endpoint, token_data, 10)

    @patch('djalf.managers.TokenManagerDjango._get_from_cache')
    def test_get_token_data_should_verify_if_do_have_token_data_in_cache(self, _get_from_cache):
        _get_from_cache.return_value = '{}'

        self.manager._get_token_data()

        _get_from_cache.assert_called_once()

    @patch('alf.managers.TokenManager._get_token_data')
    @patch('djalf.managers.TokenManagerDjango._get_from_cache')
    def test_get_token_data_should_call_super_class_get_token_if_does_not_have_token_data_in_cache(self, _get_from_cache, original_get_token_data):
        _get_from_cache.return_value = ''

        self.manager._get_token_data()

        original_get_token_data.assert_called_once()
