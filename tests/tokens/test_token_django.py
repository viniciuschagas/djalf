# -*- coding: utf-8 -*-
from mock import patch
from unittest import TestCase, skip

from django.conf import settings

from alf.tokens import Token
from djalf.tokens import TokenDjango


class TestTokenDjango(TestCase):
    @skip('Need settings')
    def test_should_be_a_subclass_of_Token(self):
        self.assertTrue(issubclass(TokenDjango, Token))

    @skip('Need settings')
    @patch('alf.tokens.cache')
    def test_should_store_access_token_using_django_cache(self, cache):
        TokenDjango(access_token='access_token', expires_in=0)

        cache.set.assert_called_once_with('account_access_token', 'access_token', 0)
