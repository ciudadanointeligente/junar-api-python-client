# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='junar-api-client',
    version='0.1',
    author=u'Joaquín Nuñez',
    author_email='joaquin.nunez@junar.com',
    url='https://github.com/joaquinnunez/junar-api-python-client',
    license='MIT License since v0.0.1',
    packages=['junar_api'],
    description='Unofficial API Python Client implementation for the Junar.com API, ' + \
                'a service to collect, organize, use and share data.',
    long_description=open('README.md').read(),
)


