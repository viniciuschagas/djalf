# -*- coding: utf-8 -*-
import datetime
from mock import patch
from freezegun import freeze_time
from unittest import TestCase

from alf.tokens import Token
from djalf.managers import TokenManagerDjango

DEFAULT_DATE_TIME_STR = '2013-11-28 11:00:00.000000'

class TestTokenManagerDjango(TestCase):


    @classmethod
    def setUpClass(cls):
        cls.date_time = datetime.datetime(2013, 11, 28, 11, 15, 00, 000000)
        cls.token_data = {u'access_token': u'mytoken',
                          u'token_type': u'bearer',
                          u'expires_in': 899,
                          'expires_on': cls.date_time}
        cls.manager = TokenManagerDjango(
            'http://endpoint/token', 'client_id', 'client_secret'
        )

    def setUp(self):
        self.token = Token(access_token='anoldtoken',
                           expires_on=self.token_data.get('expires_in'))

        self.manager._token = self.token

    def tearDown(self):
        self.token_data['expires_on'] = self.date_time

    @freeze_time(DEFAULT_DATE_TIME_STR)
    def test_validate_cached_data_should_return_true_if_data_is_valid(self):
        self.assertTrue(self.manager._validate_cached_data(self.token_data))

    def test_validate_cached_data_should_return_false_if_expires_on_do_not_exist(self):
        self.token_data.pop('expires_on')
        self.assertFalse(self.manager._validate_cached_data(self.token_data))

    @freeze_time(DEFAULT_DATE_TIME_STR)
    def test_validate_cached_data_should_return_false_if_expires_on_is_lower_then_now(self):
        lower_date_time = datetime.datetime(2013, 11, 28, 10, 50, 00, 000000)
        self.token_data['expires_on'] = lower_date_time
        self.assertFalse(self.manager._validate_cached_data(self.token_data))

    @freeze_time(DEFAULT_DATE_TIME_STR)
    def test_validate_cached_data_should_return_false_if_access_token_is_the_same_in_both_cache_and_token_object(self):
        self.token.access_token = self.token_data.get('access_token')
        self.assertFalse(self.manager._validate_cached_data(self.token_data))

    def test_validate_cached_data_should_return_false_if_no_token_data_is_supplied(self):
        self.assertFalse(self.manager._validate_cached_data(''))

    @patch('djalf.managers.cache.get')
    def test_get_from_cache_should_returns_data_stored_in_cache(self, cache_get):
        self.manager._get_from_cache()

        cache_get.assert_called_once_with(self.manager._token_endpoint)

    @patch('alf.managers.TokenManager._request_token')
    @patch('djalf.managers.cache.set')
    def test_request_token_should_store_token_data_in_cache(self, cache_set, _request_token):
        token_data = {'access_token': 'access_token', 'expires_in': 10}

        _request_token.return_value = token_data

        self.manager._request_token()

        cache_set.assert_called_once_with(self.manager._token_endpoint, token_data, 10)

    @freeze_time(DEFAULT_DATE_TIME_STR)
    @patch('alf.managers.TokenManager._request_token')
    @patch('djalf.managers.cache.set')
    def test_request_token_should_generate_the_expires_on_and_store_with_token_data_in_cache(self, cache_set, _request_token):
        expected_expires_on = datetime.datetime(2013, 11, 28, 11, 0, 10)
        token_data = {'access_token': 'access_token', 'expires_in': 10}

        _request_token.return_value = token_data

        token_data = self.manager._request_token()

        self.assertEqual(token_data.get('expires_on'), expected_expires_on)

        cache_set.assert_called_once_with(self.manager._token_endpoint, token_data, 10)

    @patch('djalf.managers.log.info')
    @patch('alf.managers.TokenManager._request_token')
    @patch('djalf.managers.cache.set')
    def test_request_token_should_log_in_info_level_that_will_retrieve_a_new_token(self, cache_set, _request_token, log_info):
        _request_token.return_value = {'access_token': 'access_token', 'expires_in': 10}

        self.manager._request_token()

        log_info.assert_called_once_with('Getting a new token')


    @patch('djalf.managers.TokenManagerDjango._validate_cached_data')
    @patch('djalf.managers.TokenManagerDjango._get_from_cache')
    def test_get_token_data_should_verify_if_data_in_cache_is_valid(self, _get_from_cache, _validate_cached_data):
        _get_from_cache.return_value = self.token_data
        self.manager._get_token_data()

        _validate_cached_data.assert_called_once_with(self.token_data)

    @freeze_time(DEFAULT_DATE_TIME_STR)
    @patch('djalf.managers.TokenManagerDjango._get_from_cache')
    def test_get_token_data_should_return_data_from_cache_if_is_valid(self, _get_from_cache):
        _get_from_cache.return_value = self.token_data

        token_data_returned = self.manager._get_token_data()

        self.assertTrue(_get_from_cache.called)

        self.assertEqual(token_data_returned, self.token_data)

    @patch('alf.managers.TokenManager._get_token_data')
    @patch('djalf.managers.TokenManagerDjango._validate_cached_data')
    @patch('djalf.managers.TokenManagerDjango._get_from_cache')
    def test_get_token_data_should_call_super_class_get_token_if_data_in_cache_is_not_valid(self,
                                                                                            _get_from_cache,
                                                                                            _validate_cached_data,
                                                                                            original_get_token_data):
        _get_from_cache.return_value = self.token_data
        _validate_cached_data.return_value = False

        self.manager._get_token_data()

        self.assertTrue(_validate_cached_data.called)

        self.assertTrue(original_get_token_data.called)

    @patch('alf.managers.TokenManager._update_token')
    def test_reset_token_should_call_update_token_method(self, _update_token):
        self.manager.reset_token()

        self.assertTrue(_update_token.called)

    @patch('djalf.managers.log.warning')
    @patch('alf.managers.TokenManager._update_token')
    def test_reset_token_should_log_an_warning_about_it(self, _update_token, log_warning):
        self.manager.reset_token()

        log_warning.assert_called_once_with('Starting token reset process')

    def test_cache_key_should_be_formed_by_endpoint_client_id_and_secret(self):
        cache_key = self.manager._get_cache_key()
        self.assertEqual(cache_key,
                         'http://endpoint/token_client_id_client_secret')
