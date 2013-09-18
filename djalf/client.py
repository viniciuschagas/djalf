# -*- coding: utf-8 -*-
from alf.client import Client

from djalf.managers import TokenManagerDjango


class DjangoClient(Client):

    token_manager_class = TokenManagerDjango
