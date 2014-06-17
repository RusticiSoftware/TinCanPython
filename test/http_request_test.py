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
from tincan.http_request import HTTPRequest


class HTTPRequestTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init_empty(self):
        req = HTTPRequest()
        self.assertIsInstance(req, HTTPRequest)
        self.assertFalse(hasattr(req, "endpoint"))
        self.assertFalse(hasattr(req, "content"))
        self.assertFalse(hasattr(req, "ignore404"))

        self.assertTrue(hasattr(req, "method"))
        self.assertIsNone(req.method)

        self.assertTrue(hasattr(req, "resource"))
        self.assertIsNone(req.resource)

        self.assertTrue(hasattr(req, "headers"))
        self.assertEqual(req.headers, {})

        self.assertTrue(hasattr(req, "query_params"))
        self.assertEqual(req.query_params, {})

    def test_init_kwarg_exception(self):
        with self.assertRaises(AttributeError):
            HTTPRequest(bad_test="test")

    def test_init_arg_exception_dict(self):
        d = {"bad_test": "test", "endpoint": "ok"}
        with self.assertRaises(AttributeError):
            HTTPRequest(d)

    def test_init_arg_exception_obj(self):
        class Tester(object):
            def __init__(self, endpoint="ok", bad_test="test"):
                self.endpoint = endpoint
                self.bad_test = bad_test

        obj = Tester()

        with self.assertRaises(AttributeError):
            HTTPRequest(obj)

    def test_init_partial(self):
        req = HTTPRequest(
            endpoint="endpoint test",
            method="method test",
            query_params={"test": "val"}
        )
        self.assertIsInstance(req, HTTPRequest)

        self.assertEqual(req.endpoint, "endpoint test")
        self.assertEqual(req.method, "method test")
        self.assertEqual(req.query_params, {"test": "val"})

        self.assertFalse(hasattr(req, "content"))
        self.assertFalse(hasattr(req, "ignore404"))

        self.assertTrue(hasattr(req, "resource"))
        self.assertIsNone(req.resource)

        self.assertTrue(hasattr(req, "headers"))
        self.assertEqual(req.headers, {})

    def test_init_all(self):
        req = HTTPRequest(
            endpoint="endpoint test",
            method="method test",
            resource="resource test",
            headers={"test": "val"},
            query_params={"test": "val"},
            content="content test",
            ignore404=True,
        )
        self.assertIsInstance(req, HTTPRequest)

        self.assertEqual(req.endpoint, "endpoint test")
        self.assertEqual(req.method, "method test")
        self.assertEqual(req.resource, "resource test")
        self.assertEqual(req.headers, {"test": "val"})
        self.assertEqual(req.query_params, {"test": "val"})
        self.assertEqual(req.content, "content test")
        self.assertTrue(req.ignore404)

    def test_setters(self):
        req = HTTPRequest()

        req.endpoint = "endpoint test"
        req.method = "method test"
        req.resource = "resource test"
        req.headers = {"test": "val"}
        req.query_params = {"test": "val"}
        req.content = "content test"
        req.ignore404 = True

        self.assertIsInstance(req, HTTPRequest)

        self.assertEqual(req.endpoint, "endpoint test")
        self.assertEqual(req.method, "method test")
        self.assertEqual(req.resource, "resource test")
        self.assertEqual(req.headers, {"test": "val"})
        self.assertEqual(req.query_params, {"test": "val"})
        self.assertEqual(req.content, "content test")
        self.assertTrue(req.ignore404)

    def test_setters_none(self):
        req = HTTPRequest()

        req.endpoint = None
        req.method = None
        req.resource = None
        req.headers = None
        req.query_params = None
        req.content = None
        req.ignore404 = None

        self.assertIsInstance(req, HTTPRequest)

        self.assertTrue(hasattr(req, "endpoint"))
        self.assertIsNone(req.endpoint)

        self.assertTrue(hasattr(req, "content"))
        self.assertIsNone(req.content)

        self.assertTrue(hasattr(req, "ignore404"))
        self.assertFalse(req.ignore404)

        self.assertTrue(hasattr(req, "method"))
        self.assertIsNone(req.method)

        self.assertTrue(hasattr(req, "resource"))
        self.assertIsNone(req.resource)

        self.assertTrue(hasattr(req, "headers"))
        self.assertEqual(req.headers, {})

        self.assertTrue(hasattr(req, "query_params"))
        self.assertEqual(req.query_params, {})

    def test_headers_setter(self):
        class Tester(object):
            def __init__(self, param="ok", tester="test"):
                self.param = param
                self.tester = tester

        obj = Tester()
        req = HTTPRequest(headers=obj)

        self.assertIsInstance(req, HTTPRequest)
        self.assertIsInstance(req.headers, dict)
        self.assertTrue("param" in req.headers)
        self.assertEqual(req.headers["param"], "ok")
        self.assertTrue("tester" in req.headers)
        self.assertEqual(req.headers["tester"], "test")

    def test_query_params_setter(self):
        class Tester(object):
            def __init__(self, param="ok", tester="test"):
                self.param = param
                self.tester = tester

        obj = Tester()
        req = HTTPRequest(query_params=obj)

        self.assertIsInstance(req, HTTPRequest)
        self.assertIsInstance(req.query_params, dict)
        self.assertTrue("param" in req.query_params)
        self.assertEqual(req.query_params["param"], "ok")
        self.assertTrue("tester" in req.query_params)
        self.assertEqual(req.query_params["tester"], "test")

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(HTTPRequestTest)
    unittest.TextTestRunner(verbosity=2).run(suite)