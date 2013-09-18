# -*- coding: utf-8 -*-
from alf.tokens import Token


class TokenDjango(Token):
    def __init__(self, access_token='', expires_in=0):
        self.access_token = access_token

        super(TokenDjango, self).__init__(access_token=access_token, expires_in=expires_in)

    @property
    def access_token(self):
        pass

    @access_token.setter
    def access_token(self, access_token):
        pass

    def is_valid(self):
        pass
