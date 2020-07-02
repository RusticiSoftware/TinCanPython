from setuptools import setup


def load_requirements(*requirements_paths):
    """
    Load all requirements from the specified requirements files.
    Returns a list of requirement strings.
    """
    requirements = set()
    for path in requirements_paths:
        with open(path) as reqs:
            requirements.update(
                line.split('#')[0].strip() for line in reqs
                if is_requirement(line.strip())
            )
    return list(requirements)


def is_requirement(line):
    """
    Return True if the requirement line is a package requirement;
    that is, it is not blank, a comment, a URL, or an included file.
    """
    return line and not line.startswith(('-r', '#', '-e', 'git+', '-c'))


setup(
    name='edx-tincan-py35',
    packages=[
        'tincan',
        'tincan/conversions',
        'tincan/documents',
    ],
    version='0.0.6',
    description='A Python 3 library for implementing Tin Can API.',
    author='edX',
    author_email='oscm@edx.org',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.8',
    ],
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
    install_requires=load_requirements('requirements/base.in'),
)
