#!/usr/bin/env python

import unittest
from datetime import timedelta

from TinCanPython.score import Score
from TinCanPython.extensions import Extensions
from TinCanPython.result import Result
from test_utils import TinCanBaseTestCase


class ScoreTest(TinCanBaseTestCase):
    def setUp(self):
        self.score = Score(max=100.0, min=0.0, raw=80.0, scaled=0.8)
        self.extensions = Extensions({'http://example.com/extension': 'extension value', })

    def test_serialize_deserialize(self):
        res = Result()
        res.completion = True
        res.duration = timedelta(seconds=1.75)
        res.extensions = self.extensions
        res.response = "Heres a response"
        res.score = self.score
        res.success = False

        self.assertSerializeDeserialize(res)

    def test_serialize_deserialize_init(self):
        data = {
            'completion': True,
            'duration': timedelta(seconds=1.75),
            'extensions': self.extensions,
            'response': "Here's a response",
            'score': self.score,
            'success': False,
        }
        res = Result(**data)

        self.assertSerializeDeserialize(res)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ScoreTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
