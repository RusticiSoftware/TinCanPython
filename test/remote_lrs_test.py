import unittest
from TinCanPython.remote_lrs import RemoteLRS
from TinCanPython.lrs_response import LRSResponse
from TinCanPython.versions import Version
from resources import lrs_properties


class RemoteLRSTest(unittest.TestCase):

    def __init__(self):
        self.endpoint = lrs_properties.endpoint
        self.version = lrs_properties.version
        self.username = lrs_properties.username
        self.password = lrs_properties.password
        self.lrs = RemoteLRS(self.version, self.endpoint, username=self.username, password=self.password)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_instantiation(self):
        lrs = RemoteLRS()
        self.assertIsInstance(lrs, RemoteLRS)
        self.assertIsNone(lrs.get_endpoint())
        self.assertIsNone(lrs.get_auth())
        self.assertEqual(Version.latest, lrs.get_version())

    def test_about(self):
        response = self.lrs.about()

        self.assertIsInstance(response, LRSResponse)
        self.assertTrue(response.success)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(RemoteLRSTest)
    unittest.TextTestRunner(verbosity=2).run(suite)