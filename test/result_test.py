#!/usr/bin/env python

import unittest
from datetime import timedelta

from tincan.score import Score
from tincan.extensions import Extensions
from tincan.result import Result
from test_utils import TinCanBaseTestCase


class ResultTest(TinCanBaseTestCase):
    def setUp(self):
        self.score = Score(max=100.0, min=0.0, raw=80.0, scaled=0.8)
        self.extensions = Extensions({'http://example.com/extension': 'extension value', })

    def test_serialize_deserialize(self):
        res = Result()
        res.completion = True
        ##TODO: add converters for ISO 8601 duration <-> timedelta
        # res.duration = timedelta(seconds=1.75)
        res.duration = 'P1.75S'     # ISO 8601
        res.extensions = self.extensions
        res.response = "Here's a response"
        res.score = self.score
        res.success = False

        self.assertSerializeDeserialize(res)

    def test_serialize_deserialize_init(self):
        data = {
            'completion': True,
            ##TODO: add converters for ISO 8601 duration <-> timedelta
            # 'duration': timedelta(seconds=1.75),
            'duration': 'P1.75S',   # ISO 8601
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
