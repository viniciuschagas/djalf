# -*- coding: utf-8 -*-
from datetime import datetime

from django.core.cache import cache
from alf.tokens import Token


class TokenDjango(Token):

    def __init__(self, access_token='', expires_in=0):
        super(TokenDjango, self).__init__(access_token=access_token, expires_in=expires_in)

        self.access_token = access_token

    @property
    def access_token(self):
        return cache.get('account_access_token')

    @access_token.setter
    def access_token(self, access_token):
        cache.set('account_access_token', access_token, self.expires_in)

    def is_valid(self):
        return cache.get('account_access_token') and (self._expires_on >= datetime.now())
