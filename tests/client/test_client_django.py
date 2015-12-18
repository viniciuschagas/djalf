# -*- coding: utf-8 -*-
from unittest import TestCase

from django.core.cache import cache
from alf.client import Client
from djalf.client import ClientDjango


class TestClientDjango(TestCase):

    def test_client_django_should_be_subclass_of_class(self):
        self.assertTrue(issubclass(ClientDjango, Client))

    def test_client_django_should_redefine_token_storage_to_token_manager_django(self):
        client = ClientDjango(token_endpoint='test_endpoint',
                              client_id='client_id',
                              client_secret='client_secret')
        self.assertEqual(client._token_storage, cache)
