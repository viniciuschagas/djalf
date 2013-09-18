# -*- coding: utf-8 -*-
from alf.managers import TokenManager
from djalf.tokens import TokenDjango


class TokenManagerDjango(TokenManager):

    def __init__(self, *args, **kwargs):
        super(TokenManagerDjango, self).__init__(*args, **kwargs)

        self._token = TokenDjango()
