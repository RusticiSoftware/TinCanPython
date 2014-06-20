A Python library for implementing Tin Can API.

For hosted API documentation, basic usage instructions, supported version listing, etc. visit the main project website at:

http://rusticisoftware.github.io/TinCanPython/

For more information about the Tin Can API visit:

http://tincanapi.com/

Requires Python 2.7 or later.

### Installation

### Testing
The preferred way to run the tests is from the command line. 

#### On Windows
On Windows, make sure that your Python installation allows you to run Python from the command line. If not:

1. Run the Python installer again.
2. Choose "Change Python" from the list.
3. Include "Add python.exe to Path" in the install options. I.e. install everything.
4. Click "Next," then "Finish."

#### Running the tests
It is possible to run all the tests in one go, or just run one part of the tests to verify a single part of `tincan`. The tests are located in the `test` directory of your `tincan` package installation.

* All the tests:
    
    1. `cd` to the `test` directory.  
    2. Run
    
        python main.py

* One of the tests:
    
    1. `cd` to the directory containing the test.
    2. Run
    
        python result_test.py
    
    (or whatever test you want to run)

### API doc generation
To automatically generate documentation, run the command 

    sphinx-apidoc -o ./docs/source/ tincan/

from the TinCanPython directory. Then from the TinCanPython/docs folder run 

    make html

The docs will be put in TinCanPython/docs/build/html/index.html. 

If you would like to change the names of each section, you can do so by modifying TinCanPython/docs/source/tincan.rst.

### Releasing
