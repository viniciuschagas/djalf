# -*- coding: utf-8 -*-
import logging
from datetime import datetime, timedelta
from django.core.cache import cache
from alf.managers import TokenManager

log = logging.getLogger(__name__)


class TokenManagerDjango(TokenManager):

    def _get_cache_key(self):
        return '{}_{}_{}'.format(self._token_endpoint, self._client_id,
                                 self._client_secret)

    def _get_from_cache(self):
        return cache.get(self._get_cache_key())

    def _validate_cached_data(self, token_data):
        if token_data:
            expires_on = token_data.get('expires_on', None)
            if (expires_on and expires_on > datetime.now()) and (self._token.access_token != token_data.get('access_token')):
                return True

        return False

    def reset_token(self):
        log.warning('Starting token reset process')
        self._update_token()

    def _get_token_data(self):
        token_data = self._get_from_cache()
        is_valid = self._validate_cached_data(token_data)

        if is_valid:
            return token_data

        return super(TokenManagerDjango, self)._get_token_data()

    def _request_token(self):
        log.info('Getting a new token')
        token_data = super(TokenManagerDjango, self)._request_token()
        token_data['expires_on'] = datetime.now() + timedelta(seconds=token_data.get('expires_in', 0))
        cache.set(self._get_cache_key(), token_data, token_data.get('expires_in', 0))
        return token_data
