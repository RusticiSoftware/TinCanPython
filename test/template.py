#!/usr/bin/env python

import unittest
#from resources import lrs_properties

def raise_exception(*args, **kwargs):
    print "Called raise_exception({args}, {kwargs})" % (args, kwargs)
    raise Exception()


# TODO
class TemplateTest(unittest.TestCase):

    def setUp(self):
        # Set up variables before each test
        pass

    def tearDown(self):
        # Tear down variables after each test
        pass

    def test_asserts(self):
        self.assertTrue(True, "True should be true!")
        self.assertFalse(False, "False should be false!")
        self.assertEquals(1, 1, "1 should equal 1!")
        self.assertNotEqual(1, 2, "1 should not equal 2!")
        self.assertRaises(Exception, raise_exception, 1, 2, c=3, d=4)

    def test_sanity(self):
        self.assertEquals(1+1, 2, "INSANITY! 1+1 != 2")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TemplateTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
