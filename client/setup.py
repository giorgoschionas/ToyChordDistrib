
from setuptools import setup, find_packages
from chordy.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='chordy',
    version=VERSION,
    description='CLI application that gives access to a distributed song database based on Chord protocol',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Snorg',
    author_email='giannissterg@hotmail.com',
    url='https://github.com/giorgoschionas/ToyChordDistrib',
    license='unlicensed',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'chordy': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        chordy = chordy.main:main
    """,
)
