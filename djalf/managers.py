# -*- coding: utf-8 -*-
from django.core.cache import cache
from alf.managers import TokenManager


class TokenManagerDjango(TokenManager):

    def _get_from_cache(self):
        return cache.get(self._token_endpoint)

    def _get_token_data(self):
        token_data = self._get_from_cache()
        if token_data:
            return token_data

        return super(TokenManagerDjango, self)._get_token_data()

    def _request_token(self):
        token_data = super(TokenManagerDjango, self)._request_token()
        cache.set(self._token_endpoint, token_data, token_data.get('expires_in', 0))
        return token_data
