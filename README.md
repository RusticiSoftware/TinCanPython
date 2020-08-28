A Python library for implementing Tin Can API.

[![Build Status](https://travis-ci.org/RusticiSoftware/TinCanPython.png)](https://travis-ci.org/RusticiSoftware/TinCanPython)

For hosted API documentation, basic usage instructions, supported version listing, etc. visit the main project website at:

<http://rusticisoftware.github.io/TinCanPython/>

For more information about the Tin Can API visit:

<http://tincanapi.com/>

Requires Python 3.6 or later.

## Installation
TinCanPython requires [Python 3.6](https://www.python.org/downloads/) or later.

If you are installing from the Github repo, you will need to install `aniso8601` and `pytz` (use `sudo` as necessary):

    pip3 install aniso8601 pytz

## Testing
The preferred way to run the tests is from the command line.

### Unix-like systems and Mac OS X
No preparation needed.

### Windows
Make sure that your Python installation allows you to run `python` from the command line. If not:

1. Run the Python installer again.
2. Choose "Change Python" from the list.
3. Include "Add python.exe to Path" in the install options. I.e. install everything.
4. Click "Next," then "Finish."

### Running the tests
It is possible to run all the tests in one go, or just run one part of the tests to verify a single part of TinCanPython. The tests are located in `test/`.

#### All the tests:
1. `cd` to the `test` directory.
2. Run

        python3 main.py

#### One of the tests:
1. `cd` to the root directory.
2. Run

        python3 -m unittest test.remote_lrs_test
    Where "remote_lrs_test.py" is the test file you want to run


#### A single test case of one of the tests:
1. `cd` to the root directory.
2. Run

        python3 -m unittest test.remote_lrs_test.RemoteLRSTest.test_save_statements

    Where "remote_lrs_test" is the test file, "RemoteLRSTest" is the class in that file, and "test_save_statements" is the specific test case.

## API doc generation
To automatically generate documentation, at the root of the repository run,

    sphinx-apidoc -f -o ./docs/source/ tincan/

Then from the `docs/` directory run,

    make html

The docs will be output to `docs/build/html/`.

If you would like to change the names of each section, you can do so by modifying `docs/source/tincan.rst`.

## Releasing
To release to PyPI, first make sure that you have a PyPI account set up at https://pypi.python.org/pypi (and at
 https://testpypi.python.org/pypi if you plan on using the test index). You will also need a `.pypirc` file in your
 home directory with the following contents.

    [distutils]

    index-servers =
        pypi
        pypitest

    [pypi] # authentication details for live PyPI
    repository: https://pypi.python.org/pypi
    username: <username>
    password: <password>

    [pypitest] # authentication details for test PyPI
    repository: https://testpypi.python.org/pypi
    username: <username>
    password: <password>

The pypitest contents of the `.pypirc` file are optional and are used for hosting to the test PyPI index.

Update setup.py to contain the correct release version and any other new information.

To test the register/upload, run the following commands in the repo directory:

    python3 setup.py register -r pypitest
    python3 setup.py sdist upload -r pypitest

You should get no errors and should be able to find this tincan version at https://testpypi.python.org/pypi.

To register/upload to the live PyPI server, run the following commands in the repo directory:

    python3 setup.py register -r pypi
    python3 setup.py sdist upload -r pypi

The new module should be now be installable with pip.

    pip3 install tincan
    
Use sudo as necessary.
