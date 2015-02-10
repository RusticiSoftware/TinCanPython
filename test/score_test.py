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

if __name__ == '__main__':
    from main import setup_tincan_path

    setup_tincan_path()
from tincan import Score
from test_utils import TinCanBaseTestCase


class ScoreTest(TinCanBaseTestCase):
    def test_serialize_deserialize(self):
        s = Score()
        s.max = 100.0
        s.min = 0.0
        s.raw = 80.0
        s.scaled = 0.8

        self.assertSerializeDeserialize(s)

    def test_serialize_deserialize_init(self):
        s = Score(max=100.0, min=0.0, raw=80.0, scaled=0.8)

        self.assertSerializeDeserialize(s)

    def test_bad_property_init(self):
        with self.assertRaises(AttributeError):
            Score(bad_name=2)

        with self.assertRaises(AttributeError):
            Score({'bad_name': 2})


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ScoreTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
