# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='django-alf',
    version='0.1',
    description="OAuth Client",
    long_description='Django cache layer to alf, a OAuth Client based on requests.Session with seamless support for Client Credentials Flow',
    keywords='oauth client client_credentials requests django',
    author=u'Globo.com',
    author_email='j3@corp.globo.com',
    url='https://github.com/globocom/django-alf',
    license='Proprietary',
    classifiers=['Intended Audience :: Developers'],
    packages=find_packages(
        exclude=(
            'tests',
        ),
    ),
    include_package_data=True,
    install_requires=[
        'alf>=0.2',
        'Django>=1.4.0'
    ],
)
