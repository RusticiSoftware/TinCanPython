A Python library for implementing Tin Can API.

For hosted API documentation, basic usage instructions, supported version listing, etc. visit the main project website at:

http://rusticisoftware.github.io/TinCanPython/

For more information about the Tin Can API visit:

http://tincanapi.com/

Requires Python 2.7 or later.

### Installation

### Testing
The preferred way to run the tests is from the command line. 

On Windows, make sure that your Python installation allows you to run Python from the command line. If not:

1. Run the Python installer again.
2. Choose "Change Python" from the list.
3. Include "Add python.exe to Path" in the install options. I.e. install everything.
4. Click "Next," then "Finish."

Before running any of the tests, make sure that `tincan` is installed or in Python's path. If you can already `import tincan`, you can skip to "Running the tests."

#### Setting up Python's path
1. To check if the `tincan` package is available, open an interactive Python shell and run:

        import tincan

    - If you don't see an error, you are set up and can exit the Python shell (type `exit()`). You can skip to the next section, "Running the tests."

    - If you do see an error, type `exit()` to exit the interpreter and continue with step 2.

2. Find the absolute path to the TinCanPython folder. Copy it to your clipboard.
3. Now, we add it to the path. This will depend on what system you are using:

##### On Unix-like systems and Mac OS X:

4. Run the following in the bash shell where you will be testing:

        export PYTHONPATH="/path/to/TinCanPython:${PYTHONPATH}"

5. If you are advanced, you can add this line to your login script (usually ~/.bashrc.)

##### On Windows:

4. Open My Computer > Properties > Advanced [System Settings] > Environment Variables.
5. In both the list for your user and for the whole system, look for the `PYTHONPATH` variable:

    - If it's there, edit it and add ";C:\\path\to\TinCanPython" to the end. The semicolon is important, since it separates the different path directories.
    
    - If it doesn't exist yet, create `PYTHONPATH` either for your user or the system and set it to "C:\\path\to\TinCanPython". No semicolon is necessary, since this is the only path present.

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
