from setuptools import setup

setup(
    name='tincan',
    packages=[
        'tincan'
    ],
    version='1.0',
    description='A Python library for implementing Tin Can API.',
    author='Rustici Software',
    author_email='mailto:info@tincanapi.com',
    url='https://github.com/RusticiSoftware/TinCanPython',
    license='Apache License 2.0',

    #TODO:this needs to be setup
    download_url='https://github.com/RusticiSoftware/TinCanPython/tarball/1.0',
    keywords=[
        'Tin Can',
        'Tin Can API',
        'Experience API'
    ],
    requires=[
      'aniso8601',
      'pytz',
    ]
)