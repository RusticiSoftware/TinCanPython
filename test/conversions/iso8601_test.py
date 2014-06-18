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
from tincan.conversions.iso8601 import make_timedelta, jsonify_timedelta
from datetime import timedelta


class ISO8601Test(unittest.TestCase):

    def test_encode_iso_to_timedelta(self):
        td = make_timedelta('PT0S')
        self.assertEqual(td.total_seconds(), 0)
        self.assertEqual(td.seconds, 0)
        self.assertEqual(td.microseconds, 0)

        td = make_timedelta('PT1M1S')
        self.assertEqual(td.total_seconds(), 61)
        self.assertEqual(td.seconds, 61)
        self.assertEqual(td.microseconds, 0)

        td = make_timedelta('PT00.225S')
        self.assertEqual(td.total_seconds(), 0.225)
        self.assertEqual(td.seconds, 0)
        self.assertEqual(td.microseconds, 225000)

        td = make_timedelta('PT12.345S')
        self.assertEqual(td.total_seconds(), 12.345)
        self.assertEqual(td.seconds, 12)
        self.assertEqual(td.microseconds, 345000)

        td = make_timedelta('PT02.5000M')
        self.assertEqual(td.total_seconds(), 150)


        td = make_timedelta('PT1H')
        self.assertEqual(td.total_seconds(), 3600)
        self.assertEqual(td.seconds, 3600)
        self.assertEqual(td.microseconds, 0)

        td = make_timedelta('PT0.5H')
        self.assertEqual(td.total_seconds(), 1800)
        self.assertEqual(td.seconds, 1800)
        self.assertEqual(td.microseconds, 0)

        td = make_timedelta('PT01H02M03.045S')
        self.assertEqual(td.total_seconds(), 3600 + 2*60 + 3.045)
        self.assertEqual(td.seconds, 3723)
        self.assertEqual(td.microseconds, 45000)

        td = make_timedelta('P1D')
        self.assertEqual(td.total_seconds(), 24*3600)

        td = make_timedelta('P00.5D')
        self.assertEqual(td.total_seconds(), 12*3600)

    def test_bad_encode_iso_to_timedelta(self):
        with self.assertRaises(ValueError):
            make_timedelta('PT0.5M0.25S')

    def test_timedelta_to_iso(self):
        iso = jsonify_timedelta(timedelta(seconds=0))
        self.assertEqual(iso, 'PT00S')

        iso = jsonify_timedelta(timedelta(seconds=1))
        self.assertEqual(iso, 'PT01S')

        iso = jsonify_timedelta(timedelta(seconds=0.05))
        self.assertEqual(iso, 'PT00.05S')

        iso = jsonify_timedelta(timedelta(seconds=60.5))
        self.assertEqual(iso, 'PT01M00.5S')

        iso = jsonify_timedelta(timedelta(seconds=7261.5))
        self.assertEqual(iso, 'PT02H01M01.5S')

        iso = jsonify_timedelta(timedelta(days=2.5))
        self.assertEqual(iso, 'P2DT12H00M00S')

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ISO8601Test)
    unittest.TextTestRunner(verbosity=2).run(suite)

