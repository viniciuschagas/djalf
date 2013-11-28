djalf
===

Djalf is an application built on top of [alf](https://github.com/globocom/alf). It implements a custom token manager that stores the access token in the django's cache backend. This is useful for applications running with more than one process (with gunicorn, for example).

Using the django's cache, the application can share the access token among Its process, reducing the number of transactions with the API.

Installation
===

First you should install [alf](https://github.com/globocom/alf)

    $ pip install -e git+https://github.com/globocom/alf#egg=alf

You can install from github:

    $ pip install -e git+https://github.com/viniciuschagas/djalf#egg=djalf

or from source:

    $ git clone https://github.com/viniciuschagas/djalf.git
    $ cd djalf
    $ python setup.py install

Usage
===

You should instantiate a django client object and use this object to perform your API calls.

    >>> from djalf.client import ClientDjango

    >>> api_client = ClientDjango(
    ...    token_endpoint='http://your-token-end-point',
    ...    client_id='your-client-id',
    ...    client_secret='you-client-secret'
    ...)

    >>> api_client.get('http://your-api-resource')
