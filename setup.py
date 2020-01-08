from setuptools import setup

setup(
    name='edx-tincan-py35',
    packages=[
        'tincan',
        'tincan/conversions',
        'tincan/documents',
    ],
    version='0.0.5',
    description='A Python 3 library for implementing Tin Can API.',
    author='edX',
    author_email='oscm@edx.org',
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
