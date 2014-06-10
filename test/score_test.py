#!/usr/bin/env python

import unittest

from tincan.score import Score
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

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ScoreTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

