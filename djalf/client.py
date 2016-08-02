# -*- coding: utf-8 -*-

from alf.client import Client
from django.core.cache import cache


__all__ = ['ClientDjango']


class ClientDjango(Client):

    def __init__(self, *args, **kwargs):
        kwargs['token_storage'] = cache
        super(ClientDjango, self).__init__(*args, **kwargs)
