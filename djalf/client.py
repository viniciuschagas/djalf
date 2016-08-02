# -*- coding: utf-8 -*-

from alf.client import Client
from django.core.cache import cache


__all__ = ['ClientDjango']


class ClientDjango(Client):

    def __init__(self, *args, **kwargs):
        super(ClientDjango, self).__init__(*args, **kwargs)
        self._token_storage = cache
