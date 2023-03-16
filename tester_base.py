import unittest
import importlib.util
import os.path
import sys
from contextlib import contextmanager
from io import StringIO

@contextmanager
def captured_output(starting_input=""):
    new_in, new_out, new_err = StringIO(starting_input), StringIO(), StringIO()
    old_in, old_out, old_err = sys.stdin, sys.stdout, sys.stderr
    try:
        sys.stdin, sys.stdout, sys.stderr = new_in, new_out, new_err
        yield sys.stdin, sys.stdout, sys.stderr
    finally:
        sys.stdin, sys.stdout, sys.stderr = new_in, old_out, old_err

class ObjectNotFoundError(Exception):
    pass

class TesterBase(unittest.TestCase):
    def setUp(self):
        """ The 'setUp' method is a frequently used method in unittest, and is called BEFORE every test case is run.
        This is useful when you want to create certain conditions before running a series of tests, without having to
        repeat code within those tests. Used in conjuction with tearDown to help ensure the test is isolated from
        the performance of other tests.

        Here it's just creating storage for any potential raised errors in the tests."""
        self.documentationErrors = []
        self.verificationErrors = []
        self.syntaxErrors = []
        print(self.id().split(".")[-1])

    def tearDown(self):
        """ The 'tearDown' is another frequently used method in unittest, and is called AFTER every test case is run.
        This is useful when you want to delete created instances or do other required tasks,
        without having to repeat code within those tests. Used in conjuction with setUp to help
        ensure the test is isolated from the performance of other tests.

        Here it's just printing off the errors that may have been stored in our list of errors, as well as the total number
        of errors.
        """
        print(self.__error_str(self.verificationErrors, "Verification"))

    def __error_str(self, error_list, error_type):
        s = ""
        for item in error_list:
            s += str(item) + "\n"
        s += f"Number of {error_type} Errors = "+str(len(error_list))
        return s
