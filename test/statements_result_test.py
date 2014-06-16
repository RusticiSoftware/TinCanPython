#!/usr/bin/env python

from tincan.statements_result import StatementsResult
from test_utils import TinCanBaseTestCase
import unittest


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

        with self.assertRaises(AttributeError):
            temp = sr.more

        sr.more = 'http://www.example.com/more/1234'

        self.assertEqual(sr.more, 'http://www.example.com/more/1234', 'Did not set more!')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(StatementsResultTest)
    unittest.TextTestRunner(verbosity=2).run(suite)