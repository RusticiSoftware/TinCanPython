from setuptools import setup

setup(
    name='tincan',
    packages=[
        'tincan',
        'tincan/conversions',
        'tincan/documents',
    ],
    version='1.0.0',
    description='A Python library for implementing Tin Can API.',
    author='Rustici Software',
    author_email='mailto:support+tincanpython@tincanapi.com',
    maintainer='Brian J. Miller',
    maintainer_email='mailto:brian.miller@tincanapi.com',
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
