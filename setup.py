try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'A math rendering bot for Slack.',
    'author': 'James',
    'version': '0.1',
    'install_requires': ['flask', 'slackclient', 'requests'],
    'packages': ['slackmath'],
    'scripts': [],
    'name': 'slackmath'
}

setup(**config)
