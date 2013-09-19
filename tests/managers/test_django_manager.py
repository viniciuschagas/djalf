# -*- coding: utf-8 -*-
from unittest import TestCase

from djalf.tokens import TokenDjango
from djalf.managers import TokenManagerDjango


class TestTokenManagerDjango(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.manager = TokenManagerDjango(
            'http://endpoint/token', 'client_id', 'client_secret'
        )

    def test_should_use_token_django(self):
        self.assertTrue(isinstance(self.manager._token, TokenDjango))
