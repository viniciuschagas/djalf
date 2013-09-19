# -*- coding: utf-8 -*-
from unittest import TestCase

from alf.client import Client
from djalf.client import ClientDjango
from djalf.managers import TokenManagerDjango


class TestClientDjango(TestCase):

    def test_client_django_should_be_subclass_of_class(self):
        self.assertTrue(issubclass(ClientDjango, Client))

    def test_client_django_should_redefine_token_manager_to_token_manager_django(self):
        self.assertEqual(ClientDjango.token_manager_class, TokenManagerDjango)
