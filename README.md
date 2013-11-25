djalf
===

Djalf is an application built on top of [alf](https://github.com/globocom/alf). It implements a custom token manager that stores the access token in the django's cache backend. This is useful for applications running with more than one process (with gunicorn, for example).

Using the django's cache the application can share the access token among Its process and reduce the number of transactions with the API.

Usage
===

You should instanciate a django client object and use this object to perform your API calls.

    >>> from djalf.client import ClientDjango

    >>> api_client = ClientDjango(
    ...    token_endpoint='http://your-token-end-point',
    ...    client_id='your-client-id',
    ...    client_secret='you-client-secret'
    ...)


    api_client.get('http://your-api-resource')
