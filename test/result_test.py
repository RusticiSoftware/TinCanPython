# Copyright 2014 Rustici Software
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
from datetime import timedelta

if __name__ == '__main__':
    from main import setup_tincan_path

    setup_tincan_path()
from tincan import Score, Extensions, Result
from test_utils import TinCanBaseTestCase


class ResultTest(TinCanBaseTestCase):
    def setUp(self):
        self.score = Score(max=100.0, min=0.0, raw=80.0, scaled=0.8)
        self.extensions = Extensions({'http://example.com/extension': 'extension value', })

    def test_serialize_deserialize(self):
        res = Result()
        res.completion = True
        res.duration = timedelta(seconds=1.75)
        # res.duration = 'PT1.75S'     # ISO 8601
        res.extensions = self.extensions
        res.response = "Here's a response"
        res.score = self.score
        res.success = False

        self.assertSerializeDeserialize(res)

    def test_serialize_deserialize_init(self):
        data = {
            'completion': True,
            'duration': timedelta(seconds=1.75),
            # 'duration': 'PT1.75S',   # ISO 8601
            'extensions': self.extensions,
            'response': "Here's a response",
            'score': self.score,
            'success': False,
        }
        res = Result(**data)

        self.assertSerializeDeserialize(res)

    def test_bad_property_init(self):
        with self.assertRaises(AttributeError):
            Result(bad_name=2)

        with self.assertRaises(AttributeError):
            Result({'bad_name': 2})


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ResultTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
