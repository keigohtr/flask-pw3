#!/usr/bin/env python

import re
from os import path as op

from setuptools import setup


def _read(fname):
    try:
        return open(op.join(op.dirname(__file__), fname)).read()
    except IOError:
        return ''

_meta = _read('flask_pw/__init__.py')
_license = re.search(r'^__license__\s*=\s*"(.*)"', _meta, re.M).group(1)
_project = re.search(r'^__project__\s*=\s*"(.*)"', _meta, re.M).group(1)
_version = re.search(r'^__version__\s*=\s*"(.*)"', _meta, re.M).group(1)

install_requires = [
    l for l in _read('requirements.txt').split('\n')
    if l and not l.startswith('#') and not l.startswith('-')]

setup(
    name=_project,
    version=_version,
    license=_license,
    description='Peewee ORM integration for Flask framework',
    long_description_content_type='text/x-rst',
    long_description=_read('README.rst'),
    platforms=('Any'),
    keywords = "flask peewee migrations migrate signals".split(), # noqa

    author='Keigo Hattori',
    author_email='keigoht@gmail.com',
    url='https://github.com/keigohtr/flask-pw3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
    ],

    packages=['flask_pw'],
    include_package_data=True,
    install_requires=install_requires,
)
