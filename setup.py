"""Packaging settings."""


from codecs import open
from os.path import abspath, dirname, join
from subprocess import call

from setuptools import Command, setup

from cmapp import __version__

"""
The script uses README.rst file for documentation

"""


this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.rst'), encoding='utf-8') as file:
    long_description = file.read()


class RunTests(Command):
    """
    This class Run all tests to test this package using py.test and coverage reporting

    """
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run all tests!"""
        errno = call(['py.test', '--cov=skele', '--cov-report=term-missing'])
        raise SystemExit(errno)


setup(
    name = 'cmapp',
    version = __version__,
    description = 'A Contacts Manager command line program in Python.',
    long_description = long_description,
    url = 'https://github.com/crakama/ContactsManager',
    author = 'Catherine Rakama',
    author_email = 'crakama89@gmail.com',
    license = 'UNLICENSE',
    classifiers = [
        'Intended Audience :: Developers',
        'Topic :: Python Console Using Docopt',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords = 'cmapp',
    packages = [ 'cmapp', 'tests*'],
    install_requires = ['docopt'],
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    entry_points = {
        'console_scripts': [
            'cmapp=cmapp.cli_entrypoint:main',
        ],
    },
    cmdclass = {'test': RunTests},
)
