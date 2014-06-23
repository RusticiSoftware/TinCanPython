#    Copyright 2014 Rustici Software
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import unittest
import datetime
import pytz

if __name__ == '__main__':
    import sys
    from os.path import dirname, abspath
    sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))
    from test.main import setup_tincan_path
    setup_tincan_path()
from tincan.documents import Document


class DocumentTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init_empty(self):
        doc = Document()
        self.assertIsInstance(doc, Document)
        self.assertTrue(hasattr(doc, "id"))
        self.assertIsNone(doc.id)
        self.assertTrue(hasattr(doc, "content_type"))
        self.assertIsNone(doc.content_type)
        self.assertTrue(hasattr(doc, "content"))
        self.assertIsNone(doc.content)
        self.assertTrue(hasattr(doc, "etag"))
        self.assertIsNone(doc.etag)
        self.assertTrue(hasattr(doc, "time_stamp"))
        self.assertIsNone(doc.time_stamp)

    def test_init_kwarg_exception(self):
        with self.assertRaises(AttributeError):
            Document(bad_test="test")

    def test_init_arg_exception_dict(self):
        d = {"bad_test": "test", "id": "ok"}
        with self.assertRaises(AttributeError):
            Document(d)

    def test_init_arg_exception_obj(self):
        class Tester(object):
            def __init__(self, id=None, bad_test="test"):
                self.id = id
                self.bad_test = bad_test

        obj = Tester()

        with self.assertRaises(AttributeError):
            Document(obj)

    def test_init_partial(self):
        doc = Document(id="test", content_type="test type")
        self.assertEqual(doc.id, "test")
        self.assertEqual(doc.content_type, "test type")
        self.assertTrue(hasattr(doc, "content"))
        self.assertTrue(hasattr(doc, "etag"))
        self.assertTrue(hasattr(doc, "time_stamp"))

    def test_init_all(self):
        doc = Document(
            id="test",
            content_type="test type",
            content=bytearray("test bytearray", "utf-8"),
            etag="test etag",
            time_stamp="2014-06-23T15:25:00-05:00"
        )

        self.assertEqual(doc.id, "test")
        self.assertEqual(doc.content_type, "test type")
        self.assertEqual(doc.content, bytearray("test bytearray", "utf-8"))
        self.assertEqual(doc.etag, "test etag")

        central = pytz.timezone("US/Central")   # UTC -0500
        dt = central.localize(datetime.datetime(2014, 6, 23, 15, 25))
        self.assertEqual(doc.time_stamp, dt)

    def test_setters(self):
        doc = Document()
        doc.id = "test"
        doc.content_type = "test type"
        doc.content = bytearray("test bytearray", "utf-8")
        doc.etag = "test etag"
        doc.time_stamp = "2014-06-23T15:25:00-05:00"

        self.assertEqual(doc.id, "test")
        self.assertEqual(doc.content_type, "test type")
        self.assertEqual(doc.content, bytearray("test bytearray", "utf-8"))
        self.assertEqual(doc.etag, "test etag")

        central = pytz.timezone("US/Central")   # UTC -0500
        dt = central.localize(datetime.datetime(2014, 6, 23, 15, 25))
        self.assertEqual(doc.time_stamp, dt)

    def test_setters_none(self):
        doc = Document()
        doc.id = None
        doc.content_type = None
        doc.content = None
        doc.etag = None
        doc.time_stamp = None

        self.assertIsNone(doc.id)
        self.assertIsNone(doc.content_type)
        self.assertIsNone(doc.content)
        self.assertIsNone(doc.etag)
        self.assertIsNone(doc.time_stamp)

    def test_content_setter(self):
        doc = Document()
        doc.content = "test bytearray"
        self.assertEqual(doc.content, bytearray("test bytearray", "utf-8"))

    def test_content_time_stamp(self):
        doc = Document()
        dt = datetime.datetime.now()
        doc.time_stamp = dt
        self.assertEqual(doc.time_stamp, dt)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(DocumentTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
