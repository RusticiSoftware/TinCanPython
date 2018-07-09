# coding=utf-8
#
# Copyright 2014 Rustici Software
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless respuired by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import unittest

from six import string_types

try:
    import http.client as httplib
except ImportError:
    import httplib

if __name__ == '__main__':
    from main import setup_tincan_path

    setup_tincan_path()
from tincan import LRSResponse, HTTPRequest


class LRSResponseTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init_empty(self):
        resp = LRSResponse()
        self.assertIsInstance(resp, LRSResponse)
        self.assertIsNone(resp.content)

        self.assertTrue(hasattr(resp, "success"))
        self.assertFalse(resp.success)

        self.assertTrue(hasattr(resp, "request"))
        self.assertIsNone(resp.request)

        self.assertTrue(hasattr(resp, "response"))
        self.assertIsNone(resp.response)

    def test_init_kwarg_exception(self):
        with self.assertRaises(AttributeError):
            LRSResponse(bad_test="test")

    def test_init_arg_exception_dict(self):
        d = {"bad_test": "test", "content": "ok"}
        with self.assertRaises(AttributeError):
            LRSResponse(d)

    def test_init_arg_exception_obj(self):
        class Tester(object):
            def __init__(self, success=True, bad_test="test"):
                self.success = success
                self.bad_test = bad_test

        obj = Tester()

        with self.assertRaises(AttributeError):
            LRSResponse(obj)

    def test_init_partial(self):
        req = HTTPRequest(resource="test")

        resp = LRSResponse(
            success=True,
            content="content test",
            request=req,
        )
        self.assertIsInstance(resp, LRSResponse)

        self.assertTrue(resp.success)
        self.assertEqual(resp.content, "content test")
        self.assertIsInstance(resp.request, HTTPRequest)
        self.assertEqual(resp.request, req)

        self.assertTrue(hasattr(resp, "response"))
        self.assertIsNone(resp.response)

    def test_init_all(self):
        conn = httplib.HTTPConnection("tincanapi.com")
        conn.request("GET", "")
        web_resp = conn.getresponse()

        req = HTTPRequest(resource="test")

        resp = LRSResponse(
            success=True,
            content="content test",
            request=req,
            response=web_resp,

        )
        self.assertIsInstance(resp, LRSResponse)

        self.assertTrue(resp.success)
        self.assertEqual(resp.content, "content test")
        self.assertIsInstance(resp.request, HTTPRequest)
        self.assertEqual(resp.request, req)

        self.assertIsInstance(resp.response, httplib.HTTPResponse)
        self.assertEqual(resp.response, web_resp)

    def test_setters(self):
        conn = httplib.HTTPConnection("tincanapi.com")
        conn.request("GET", "")
        web_resp = conn.getresponse()

        req = HTTPRequest(resource="test")

        resp = LRSResponse()
        resp.success = True
        resp.content = "content test"
        resp.request = req
        resp.response = web_resp

        self.assertIsInstance(resp, LRSResponse)

        self.assertTrue(resp.success)
        self.assertEqual(resp.content, "content test")
        self.assertIsInstance(resp.request, HTTPRequest)
        self.assertEqual(resp.request, req)
        self.assertEqual(resp.request.resource, "test")

        self.assertIsInstance(resp.response, httplib.HTTPResponse)
        self.assertEqual(resp.response, web_resp)

    def test_unicode(self):
        resp = LRSResponse()
        resp.data = b"\xce\xb4\xce\xbf\xce\xba\xce\xb9\xce\xbc\xce\xae " \
                    b"\xcf\x80\xce\xb5\xcf\x81\xce\xb9\xce\xb5\xcf\x87" \
                    b"\xce\xbf\xce\xbc\xce\xad\xce\xbd\xce\xbf\xcf\x85"

        self.assertIsInstance(resp, LRSResponse)
        self.assertIsInstance(resp.data, string_types)
        self.assertEqual(resp.data, u"δοκιμή περιεχομένου")

    def test_setters_none(self):
        resp = LRSResponse()

        resp.success = None
        resp.content = None
        resp.request = None
        resp.response = None

        self.assertIsInstance(resp, LRSResponse)

        self.assertTrue(hasattr(resp, "content"))
        self.assertIsNone(resp.content)

        self.assertTrue(hasattr(resp, "success"))
        self.assertFalse(resp.success)

        self.assertTrue(hasattr(resp, "request"))
        self.assertIsNone(resp.request)

        self.assertTrue(hasattr(resp, "response"))
        self.assertIsNone(resp.response)

    def test_request_setter(self):
        class Tester(object):
            def __init__(self, resource="ok", headers=None):
                if headers is None:
                    headers = {"test": "ok"}

                self.resource = resource
                self.headers = headers

        obj = Tester()

        resp = LRSResponse(request=obj)

        self.assertIsInstance(resp, LRSResponse)
        self.assertIsInstance(resp.request, HTTPRequest)
        self.assertTrue(hasattr(resp.request, "resource"))
        self.assertEqual(resp.request.resource, "ok")
        self.assertTrue(hasattr(resp.request, "headers"))
        self.assertEqual(resp.request.headers, {"test": "ok"})

    def test_response_setter(self):
        class Tester(object):
            def __init__(self, msg="ok", version="test"):
                self.msg = msg
                self.version = version

        obj = Tester()
        with self.assertRaises(TypeError):
            LRSResponse(response=obj)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(LRSResponseTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
