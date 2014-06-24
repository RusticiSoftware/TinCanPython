#!/usr/bin/env python

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

if __name__ == '__main__':
    from main import setup_tincan_path
    setup_tincan_path()
from tincan.statements_result import StatementsResult
from test_utils import TinCanBaseTestCase


class StatementsResultTest(TinCanBaseTestCase):
    def test_serialize_deserialize(self):
        sr = StatementsResult()
        sr.statements = [1, 2, 3, ]
        sr.more = 'http://www.example.com/more/1234'

        self.assertSerializeDeserialize(sr)

    def test_serialize_deserialize_init(self):
        data = {
            'statements': [1, 2, 3, 4, ],
            'more': 'http://www.example.com/more/1234',
        }

        sr = StatementsResult(data)
        self.assertSerializeDeserialize(sr)

    def test_read_write(self):
        sr = StatementsResult()
        self.assertEqual(len(sr.statements), 0, 'Empty StatementsResult inited as non-empty!')

        sr.statements = (1, 2, 3,)
        self.assertIsInstance(sr.statements, list, 'Did not convert tuple to list!')

        sr.statements.append(4)
        self.assertEqual(sr.statements[3], 4, 'Did not append value!')

        self.assertIsNone(sr.more)

        sr.more = 'http://www.example.com/more/1234'

        self.assertEqual(sr.more, 'http://www.example.com/more/1234', 'Did not set sr.more!')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(StatementsResultTest)
    unittest.TextTestRunner(verbosity=2).run(suite)