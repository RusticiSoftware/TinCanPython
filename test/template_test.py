#!/usr/bin/env python

import unittest
from resources import lrs_properties


def raise_exception(*args, **kwargs):
    print "Called raise_exception({args}, {kwargs})" % (args, kwargs)
    raise Exception()


class TemplateTest(unittest.TestCase):

    def setUp(self):
        # Set up variables before each test
        #self.my_var = True
        #self.connection = lrs_setup_connection()
        pass

    def tearDown(self):
        # Tear down variables after each test
        #self.connection.close()
        pass

    def test_asserts(self):
        self.assertTrue(True, "True should be true!")
        self.assertFalse(False, "False should be false!")
        self.assertEquals(1, 1, "1 should equal 1!")
        self.assertNotEqual(1, 2, "1 should not equal 2!")
        self.assertRaises(Exception, raise_exception, 1, 2, c=3, d=4)

        d = {'a': 'My value'}
        self.assertIsInstance(d, dict, "d should be a dict!")
        self.assertIn('a', d, "d should contain 'a'!")
        self.assertNotIn('b', d, "d should not contain 'b'!")

    def test_sanity(self):
        self.assertEquals(1+1, 2, "INSANITY! 1+1 != 2")

    def test_lrs_properties(self):
        self.assertIsNotNone(lrs_properties.username)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TemplateTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
