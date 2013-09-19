# -*- coding: utf-8 -*-
from mock import patch
from unittest import TestCase

from alf.tokens import Token
from djalf.tokens import TokenDjango


class TokenDjangoTestCase(TestCase):

    def setUp(self):
        self.token = TokenDjango(access_token='access_token', expires_in=10)

    def test_should_be_a_subclass_of_Token(self):
        self.assertTrue(issubclass(TokenDjango, Token))

    @patch('djalf.tokens.cache.set')
    def test_should_store_access_token_using_django_cache(self, cache_set):
        self.token.access_token = 'new-access-token'
        cache_set.assert_called_once_with('account_access_token', 'new-access-token', 10)

    @patch('djalf.tokens.cache.get')
    def test_should_get_access_token_from_django_cache(self, cache_get):
        self.token.access_token

        cache_get.assert_called_once_with('account_access_token')

    @patch('djalf.tokens.cache.get')
    def test_should_return_token_as_invalid_if_is_not_in_cache(self, cache_get):
        cache_get.return_value = ''

        is_valid = self.token.is_valid()

        cache_get.assert_called_once_with('account_access_token')

        self.assertFalse(is_valid)

    @patch('djalf.tokens.cache.get')
    def test_should_return_token_as_invalid_if_in_cache_but_expired(self, cache_get):
        cache_get.return_value = 'access_token'
        self.token.expires_in = 0

        is_valid = self.token.is_valid()

        cache_get.assert_called_once_with('account_access_token')

        self.assertFalse(is_valid)

    @patch('djalf.tokens.cache.get')
    def test_should_return_token_as_valid_if_in_cache_and_not_expired(self, cache_get):
        cache_get.return_value = 'access_token'

        is_valid = self.token.is_valid()

        cache_get.assert_called_once_with('account_access_token')

        self.assertTrue(is_valid)
