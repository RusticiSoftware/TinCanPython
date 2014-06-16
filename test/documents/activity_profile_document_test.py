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
from tincan.documents import ActivityProfileDocument
from tincan.activity import Activity
from tincan.activity_definition import ActivityDefinition
from tincan.languagemap import LanguageMap


class ActivityProfileDocumentTest(unittest.TestCase):

    def __init__(self):
        self.activity = Activity(
            id="http://tincanapi.com/TinCanPython/Test/Unit/0",
            definition=ActivityDefinition()
        )
        self.activity.type = "http://id.tincanapi.com/activitytype/unit-test"
        self.activity.definition.name(LanguageMap({"en-US": "Python Tests"}))
        self.activity.definition.description(LanguageMap(
            {"en-US": "Unit test in the test suite for the Python library"})
        )

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init_empty(self):
        doc = ActivityProfileDocument()
        self.assertIsInstance(doc, ActivityProfileDocument)
        self.assertFalse(hasattr(doc, "id"))
        self.assertFalse(hasattr(doc, "content_type"))
        self.assertFalse(hasattr(doc, "content"))
        self.assertFalse(hasattr(doc, "etag"))
        self.assertFalse(hasattr(doc, "time_stamp"))
        self.assertFalse(hasattr(doc, "activity"))

    def test_init_kwarg_exception(self):
        with self.assertRaises(AttributeError):
            ActivityProfileDocument(bad_test="test")

    def test_init_arg_exception_dict(self):
        d = {"bad_test": "test", "id": "ok"}
        with self.assertRaises(AttributeError):
            ActivityProfileDocument(d)

    def test_init_arg_exception_obj(self):
        class Tester(object):
            def __init__(self, id=None, bad_test="test"):
                self.id = id
                self.bad_test = bad_test

        obj = Tester()

        with self.assertRaises(AttributeError):
            ActivityProfileDocument(obj)

    def test_init_partial(self):
        doc = ActivityProfileDocument(id="test", content_type="test type")
        self.assertEqual(doc.id, "test")
        self.assertEqual(doc.content_type, "test type")
        self.assertFalse(hasattr(doc, "content"))
        self.assertFalse(hasattr(doc, "etag"))
        self.assertFalse(hasattr(doc, "time_stamp"))
        self.assertFalse(hasattr(doc, "activity"))

    def test_init_all(self):
        doc = ActivityProfileDocument(
            id="test",
            content_type="test type",
            content=bytearray("test bytearray", "utf-8"),
            etag="test etag",
            time_stamp="test time_stamp",
            activity=self.activity,
        )
        self.assertEqual(doc.id, "test")
        self.assertEqual(doc.content_type, "test type")
        self.assertEqual(doc.content, bytearray("test bytearray", "utf-8"))
        self.assertEqual(doc.etag, "test etag")
        self.assertEqual(doc.time_stamp, "test time_stamp")
        self.assertEqual(doc.activity, self.activity)

    def test_setters(self):
        doc = ActivityProfileDocument()
        doc.id = "test",
        doc.content_type = "test type",
        doc.content = bytearray("test bytearray", "utf-8"),
        doc.etag = "test etag",
        doc.time_stamp = "test time_stamp"
        doc.activity=self.activity,

        self.assertEqual(doc.id, "test")
        self.assertEqual(doc.content_type, "test type")
        self.assertEqual(doc.content, bytearray("test bytearray", "utf-8"))
        self.assertEqual(doc.etag, "test etag")
        self.assertEqual(doc.time_stamp, "test time_stamp")
        self.assertEqual(doc.activity, self.activity)

    def test_setters_none(self):
        doc = ActivityProfileDocument()
        doc.id = None
        doc.content_type = None
        doc.content = None
        doc.etag = None
        doc.time_stamp = None
        doc.activity = None

        self.assertIsNone(doc.id)
        self.assertIsNone(doc.content_type)
        self.assertIsNone(doc.content)
        self.assertIsNone(doc.etag)
        self.assertIsNone(doc.time_stamp)
        self.assertIsNone(doc.activity)

    def test_activity_setter(self):
        doc = ActivityProfileDocument()
        doc.activity = {"id": "http://tincanapi.com/TinCanPython/Test/Unit/0"}

        self.assertEquals(doc.activity, Activity(id="http://tincanapi.com/TinCanPython/Test/Unit/0"))