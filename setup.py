try:
        from setuptools import setup
except ImportError:
        from distutils.core import setup

 config = {
    'description': 'A silly git repo inspector',
    'author': 'bill shelton',
    'url': 'http://tbd.com',
    'download_url': 'http://tbd.com',
    'author_email': 'bill@if.io',
    'version': '0.1',
    'install_requires': ['nose','nose-progressive'],
    'packages': ['clouseau'],
    'py_modules' :[]
    'scripts': [],
    'name': 'clouseau'
 }
                                 
 setup(**config) 
