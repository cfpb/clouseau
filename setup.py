import os
import sys
try:
        from setuptools import setup
except ImportError:
        from distutils.core import setup

config = {
    'name': 'clouseau',
    'description': 'A silly git repo inspector',
    'long_description': None ,
        # Needs to be restructed text
        # os.path.join(os.path.dirname(__file__), 'README.md').read()


    'author': 'bill shelton',
    'url': 'https://github.com/cfpb/clouseau',
    'download_url': 'http://tbd.com',
    'author_email': 'bill@if.io',
    'version': '0.2.0',
    'install_requires': ['jinja2','nose','nose-progressive'],
    'packages': ['clouseau','tests'],
    'package_data': {'clouseau': ['clients/*.py', 'patterns/*.txt', 'templates/*.html']},
    'py_modules': [],
    'scripts': ['bin/clouseau', 'bin/clouseau_thin'],
    'keywords': ['git', 'pii', 'security', 'search',
            'sensitive information'],
    'classifiers': [
            'Development Status :: -0 - Pre-Natal',
            'Environment ::  Console',
            'Intended Audience :: Developers, Security Engineers',
            'Programming Language:  Python 2.7',
            'Operating System :: OSX',
            'Operating System :: Linux',
    ]
}

setup(**config)
