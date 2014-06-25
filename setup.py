from setuptools import setup

setup(
    name='tincan',
    packages=[
        'tincan'
    ],
    version='0.0.1',
    description='A Python library for implementing Tin Can API.',
    author='Rustici Software',
    author_email='mailto:support+tincanpython@tincanapi.com',
    url='http://rusticisoftware.github.io/TinCanPython/',
    license='Apache License 2.0',
    keywords=[
        'Tin Can',
        'TinCan',
        'Tin Can API',
        'TinCanAPI',
        'Experience API',
        'xAPI',
        'SCORM',
        'AICC',
    ],
    install_requires=[
        'aniso8601',
        'pytz',
    ],
)