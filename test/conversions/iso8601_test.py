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
from datetime import timedelta, datetime

from pytz import utc, timezone


if __name__ == '__main__':
    import sys
    from os.path import dirname, abspath

    sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))
    from test.main import setup_tincan_path

    setup_tincan_path()
from tincan.conversions.iso8601 import (
    make_timedelta, jsonify_timedelta,
    make_datetime, _make_datetime, jsonify_datetime,
)


# make sure that pytz's db is loaded so that later accesses are faster.
# to avoid long startup times, run:
#       pip unzip pytz
print (
    "Loading timezone data (if this takes a few seconds, "
    "run `pip unzip pytz` to speed it up)..."
)
timezone('US/Central')


class ISO8601Test(unittest.TestCase):
    def test_iso_to_timedelta(self):
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
        self.assertEqual(td.total_seconds(), 3600 + 2 * 60 + 3.045)
        self.assertEqual(td.seconds, 3723)
        self.assertEqual(td.microseconds, 45000)

        td = make_timedelta('P1D')
        self.assertEqual(td.total_seconds(), 24 * 3600)

        td = make_timedelta('P00.5D')
        self.assertEqual(td.total_seconds(), 12 * 3600)

    def test_seconds_to_timedelta(self):
        td = make_timedelta(0)
        self.assertEqual(td.total_seconds(), 0)
        self.assertEqual(td.days, 0)
        self.assertEqual(td.seconds, 0)
        self.assertEqual(td.microseconds, 0)

        td = make_timedelta(61.5)
        self.assertEqual(td.total_seconds(), 61.5)
        self.assertEqual(td.days, 0)
        self.assertEqual(td.seconds, 61)
        self.assertEqual(td.microseconds, 500000)

        td = make_timedelta(24 * 3600 + 61.5)
        self.assertEqual(td.total_seconds(), 24 * 3600 + 61.5)
        self.assertEqual(td.days, 1)
        self.assertEqual(td.seconds, 61)
        self.assertEqual(td.microseconds, 500000)

    def test_dict_to_timedelta(self):
        td = make_timedelta({})
        self.assertEqual(td.total_seconds(), 0)
        self.assertEqual(td.days, 0)
        self.assertEqual(td.seconds, 0)
        self.assertEqual(td.microseconds, 0)

        td = make_timedelta({'seconds': 0})
        self.assertEqual(td.total_seconds(), 0)
        self.assertEqual(td.days, 0)
        self.assertEqual(td.seconds, 0)
        self.assertEqual(td.microseconds, 0)

        td = make_timedelta({'seconds': 24 * 3600 + 61.5})
        self.assertEqual(td.total_seconds(), 24 * 3600 + 61.5)
        self.assertEqual(td.days, 1)
        self.assertEqual(td.seconds, 61)
        self.assertEqual(td.microseconds, 500000)

        td = make_timedelta({'days': 1, 'seconds': 61.5})
        self.assertEqual(td.total_seconds(), 24 * 3600 + 61.5)
        self.assertEqual(td.days, 1)
        self.assertEqual(td.seconds, 61)
        self.assertEqual(td.microseconds, 500000)

        td = make_timedelta({'days': 3, 'seconds': 61, 'microseconds': 500000})
        self.assertEqual(td.total_seconds(), 3 * 24 * 3600 + 61.5)
        self.assertEqual(td.days, 3)
        self.assertEqual(td.seconds, 61)
        self.assertEqual(td.microseconds, 500000)

    def test_bad_iso_to_timedelta(self):
        with self.assertRaises(ValueError):
            make_timedelta('PT0.5M0.25S')

        with self.assertRaises(ValueError):
            make_timedelta('T0S')

        with self.assertRaises(ValueError):
            make_timedelta('PT1')

        with self.assertRaises(ValueError):
            make_timedelta('')

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

    def test_bad_timedelta_to_iso(self):
        with self.assertRaises(AssertionError):
            jsonify_timedelta(0)

        with self.assertRaises(AssertionError):
            jsonify_timedelta(0.0)

        with self.assertRaises(AssertionError):
            jsonify_timedelta(1)

        with self.assertRaises(AssertionError):
            jsonify_timedelta(1.5)

        with self.assertRaises(AssertionError):
            jsonify_timedelta('PT12H')

        with self.assertRaises(AssertionError):
            jsonify_timedelta('2014-06-19T17:03:17.361077-05:00')

        with self.assertRaises(AssertionError):
            jsonify_timedelta(('bad', 'stuff'))

    def test_iso_to_datetime(self):
        # with microseconds
        # naive
        pair = (
            '2014-06-19T16:40:22.293913',
            datetime(2014, 6, 19, 16, 40, 22, 293913)
        )
        self.assertEqual(_make_datetime(pair[0]), pair[1])

        # timezone
        pair = (
            '2014-06-19T21:55:27.934309+00:00',
            utc.localize(datetime(2014, 6, 19, 21, 55, 27, 934309)),
        )
        self.assertEqual(make_datetime(pair[0]), pair[1])

        # with integer seconds
        # naive
        pair = (
            '2014-06-19T16:40:22',
            datetime(2014, 6, 19, 16, 40, 22, 0)
        )
        self.assertEqual(_make_datetime(pair[0]), pair[1])

        # timezone
        pair = (
            '2014-06-19T21:55:27+00:00',
            utc.localize(datetime(2014, 6, 19, 21, 55, 27, 0)),
        )
        self.assertEqual(make_datetime(pair[0]), pair[1])

        # timezone other than UTC
        central = timezone('US/Central')
        pair = (
            '2014-06-19T17:03:17.361077-05:00',
            central.localize(datetime(2014, 6, 19, 17, 3, 17, 361077)),
            # Due to pytz weirdness, the following has
            # incorrect tz offset info:
            # datetime(2014, 6, 19, 17, 3, 17, 361077, tzinfo=central))
        )
        self.assertEqual(make_datetime(pair[0]), pair[1])

    def test_number_to_datetime(self):
        pair = (
            1403272847,
            utc.localize(datetime(2014, 6, 20, 14, 0, 47, 0)),
        )
        self.assertEqual(make_datetime(pair[0]), pair[1])

        pair = (
            1403272847.361077,
            utc.localize(datetime(2014, 6, 20, 14, 0, 47, 361077)),
        )
        self.assertEqual(make_datetime(pair[0]), pair[1])

    def test_dict_to_datetime(self):
        pair = (
            {'year': 2014, 'month': 12, 'day': 17, 'tzinfo': utc, },
            utc.localize(datetime(2014, 12, 17)),
        )
        self.assertEqual(make_datetime(pair[0]), pair[1])

        pair = (
            {'year': 2014, 'month': 12, 'day': 17, 'tzinfo': utc,
             'hour': 12, 'minute': 4, 'second': 3, },
            utc.localize(datetime(2014, 12, 17, 12, 4, 3, 0)),
        )
        self.assertEqual(make_datetime(pair[0]), pair[1])

        pair = (
            {'year': 2014, 'month': 12, 'day': 17,
             'hour': 12, 'minute': 4, 'second': 3,
             'microsecond': 560000, 'tzinfo': utc, },
            utc.localize(datetime(2014, 12, 17, 12, 4, 3, 560000)),
        )
        self.assertEqual(make_datetime(pair[0]), pair[1])

        # Non-UTC timezone
        central = timezone('US/Central')

        pair = (
            {'year': 2014, 'month': 12, 'day': 17, 'tzinfo': central, },
            central.localize(datetime(2014, 12, 17)),
        )
        self.assertEqual(make_datetime(pair[0]), pair[1])

        pair = (
            {'year': 2014, 'month': 12, 'day': 17, 'tzinfo': central,
             'hour': 12, 'minute': 4, 'second': 3, },
            central.localize(datetime(2014, 12, 17, 12, 4, 3, 0)),
        )
        self.assertEqual(make_datetime(pair[0]), pair[1])

        pair = (
            {'year': 2014, 'month': 12, 'day': 17,
             'hour': 12, 'minute': 4, 'second': 3,
             'microsecond': 560000, 'tzinfo': central, },
            central.localize(datetime(2014, 12, 17, 12, 4, 3, 560000)),
        )
        self.assertEqual(make_datetime(pair[0]), pair[1])

    def test_iterable_to_datetime(self):
        pair = (
            (2014, 12, 17, utc),
            utc.localize(datetime(2014, 12, 17)),
        )
        self.assertEqual(make_datetime(pair[0]), pair[1])
        self.assertEqual(make_datetime(list(pair[0])), pair[1])

        pair = (
            (2014, 12, 17, ),
            datetime(2014, 12, 17, ),
        )
        self.assertEqual(_make_datetime(pair[0]), pair[1])
        self.assertEqual(_make_datetime(list(pair[0])), pair[1])

        pair = (
            (2014, 12, 17, 5, 13, 23, 123456, utc),
            utc.localize(datetime(2014, 12, 17, 5, 13, 23, 123456)),
        )
        self.assertEqual(make_datetime(pair[0]), pair[1])
        self.assertEqual(make_datetime(list(pair[0])), pair[1])

        pair = (
            (2014, 12, 17, 5, 13, 23, 123456),
            datetime(2014, 12, 17, 5, 13, 23, 123456),
        )
        self.assertEqual(_make_datetime(pair[0]), pair[1])
        self.assertEqual(_make_datetime(list(pair[0])), pair[1])

        # Non-UTC timezone
        central = timezone('US/Central')
        pair = (
            (2014, 12, 17, central, ),
            central.localize(datetime(2014, 12, 17)),
        )
        self.assertEqual(make_datetime(pair[0]), pair[1])
        self.assertEqual(make_datetime(list(pair[0])), pair[1])

        pair = (
            (2014, 12, 17, 5, 13, 23, 123456, central),
            central.localize(datetime(2014, 12, 17, 5, 13, 23, 123456)),
        )
        self.assertEqual(make_datetime(pair[0]), pair[1])
        self.assertEqual(make_datetime(list(pair[0])), pair[1])

    # struct_time does not preserve millisecond accuracy per
    # TinCan spec, so this is disabled to discourage its use.
    #
    # def test_struct_time_to_iso(self):
    #     now = datetime.now(tz=utc)
    #     now.second = 0              # timetuple() doesn't preserve this
    #     struct = now.timetuple()    # make struct_time
    #     pair = (
    #         now.timetuple(),
    #         now,
    #     )
    #     self.assertEqual(make_datetime(pair[0]), pair[1])

    def test_datetime_to_iso(self):
        # with microseconds
        # naive
        pair = (
            '2014-06-19T16:40:22.293913',
            datetime(2014, 6, 19, 16, 40, 22, 293913)
        )
        self.assertEqual(pair[0], jsonify_datetime(pair[1]))

        # timezone
        pair = (
            '2014-06-19T21:55:27.934309+00:00',
            utc.localize(datetime(2014, 6, 19, 21, 55, 27, 934309)),
        )
        self.assertEqual(pair[0], jsonify_datetime(pair[1]))

        # integer seconds
        # naive
        pair = (
            '2014-06-19T16:40:22',
            datetime(2014, 6, 19, 16, 40, 22, 0)
        )
        self.assertEqual(pair[0], jsonify_datetime(pair[1]))

        # timezone
        pair = (
            '2014-06-19T21:55:27+00:00',
            utc.localize(datetime(2014, 6, 19, 21, 55, 27, 0)),
        )
        self.assertEqual(pair[0], jsonify_datetime(pair[1]))

        # timezone other than UTC
        central = timezone('US/Central')
        pair = (
            '2014-06-19T17:03:17.361077-05:00',
            central.localize(datetime(2014, 6, 19, 17, 3, 17, 361077)),
            # Due to pytz weirdness, the following has
            # incorrect tz offset info:
            # datetime(2014, 6, 19, 17, 3, 17, 361077, tzinfo=central))
        )
        self.assertEqual(
            pair[0],
            jsonify_datetime(pair[1]),
        )

    def test_bad_iso_to_datetime(self):
        with self.assertRaises(ValueError):
            _make_datetime('')

        with self.assertRaises(ValueError):
            _make_datetime('bad')

        with self.assertRaises(TypeError):
            _make_datetime(None)

        with self.assertRaises(ValueError):
            # used '#' instead of 'T'
            _make_datetime('2014-06-19#17:03:17.361077-05:00')

        with self.assertRaises(ValueError):
            # used '#' instead of '-'
            _make_datetime('2014-06-19T17:03#17.361077-05:00')

        with self.assertRaises(ValueError):
            # naive timestamps raise ValueError
            make_datetime('2014-06-19T16:40:22.293913')

    def test_bad_datetime_to_iso(self):
        with self.assertRaises(AssertionError):
            jsonify_datetime('2014-06-19T17:03:17.361077-05:00')

        with self.assertRaises(AssertionError):
            jsonify_datetime(0)

        with self.assertRaises(AssertionError):
            jsonify_datetime(0.0)

        with self.assertRaises(AssertionError):
            jsonify_datetime(1)

        with self.assertRaises(AssertionError):
            jsonify_datetime(1.5)

        with self.assertRaises(AssertionError):
            jsonify_datetime('2014-06-19T17:03:17.361077-05:00')

        with self.assertRaises(AssertionError):
            jsonify_datetime('PT1H')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ISO8601Test)
    unittest.TextTestRunner(verbosity=2).run(suite)
