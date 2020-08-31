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

"""
Functions for converting ``datetime.timedelta`` and
``datetime.datetime`` to and from ISO 8601 strings.
"""

import datetime
# struct_time does not preserve millisecond accuracy per
# Tin Can spec, so this is disabled to discourage its use.
# from time import mktime, struct_time
import aniso8601
from pytz import utc

def make_timedelta(value):
    """Tries to convert the given value to a :class:`datetime.timedelta`.

    Strings will be parsed as ISO 8601 durations.

    If a number is provided, it will be interpreted as the number of
    seconds.

    If a `dict` is provided, does `datetime.timedelta(**value)`.

    :param value: something to convert
    :type value: str | unicode | float | int | datetime.timedelta | dict
    :return: the value after conversion
    :rtype: datetime.timedelta

    """

    if isinstance(value, str):
        try:
            return aniso8601.parse_duration(value)
        except Exception as e:
            msg = (
                f"Conversion to datetime.timedelta failed. Could not "
                f"parse the given string as an ISO 8601 duration: "
                f"{repr(value)}\n\n"
                f"{repr(e)}"
            )
            raise ValueError(msg)

    try:
        if isinstance(value, datetime.timedelta):
            return value
        elif isinstance(value, dict):
            return datetime.timedelta(**value)
        elif isinstance(value, (float, int)):
            return datetime.timedelta(seconds=value)
        else:
            return datetime.timedelta(value)
    except Exception as e:
        msg = (
            f"Could not convert the given value of type '{value.__class__.__name__}' to a "
            f"datetime.timedelta: {repr(value)}\n\n"
            f"{repr(e)}"
        )
        raise TypeError(msg) if isinstance(e, TypeError) else ValueError(msg)


def jsonify_timedelta(value):
    """Converts a `datetime.timedelta` to an ISO 8601 duration
    string for JSON-ification.

    :param value: something to convert
    :type value: datetime.timedelta
    :return: the value after conversion
    :rtype unicode

    """

    assert isinstance(value, datetime.timedelta)

    # split seconds to larger units
    seconds = value.total_seconds()
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    days, hours, minutes = list(map(int, (days, hours, minutes)))
    seconds = round(seconds, 6)

    # build date
    date = ''
    if days:
        date = '%sD' % days

    # build time
    time = 'T'

    # hours
    bigger_exists = date or hours
    if bigger_exists:
        time += '{:02}H'.format(hours)

    # minutes
    bigger_exists = bigger_exists or minutes
    if bigger_exists:
        time += '{:02}M'.format(minutes)

    # seconds
    if seconds.is_integer():
        seconds = '{:02}'.format(int(seconds))
    else:
        # 9 chars long w/leading 0, 6 digits after decimal
        seconds = '%09.6f' % seconds
        # remove trailing zeros
        seconds = seconds.rstrip('0')

    time += '{}S'.format(seconds)

    return 'P' + date + time


def make_datetime(value):
    """Tries to convert the given value to a :class:`datetime.datetime`. If
    no timezone is given, raises a ValueError.

    Strings will be parsed as ISO 8601 timestamps.

    If a number is provided, it will be interpreted as a UNIX
    timestamp, which by definition is UTC.

    If a `dict` is provided, does `datetime.datetime(**value)`.

    If a `tuple` or a `list` is provided, does
    `datetime.datetime(*value)`. Uses the timezone in the tuple or
    list if provided.

    :param value: something to convert
    :type value: str | unicode | float | int | :class:`datetime.datetime` | dict | list | tuple
    :return: the value after conversion
    :rtype: :class:`datetime.datetime`
    :raises: ValueError | TypeError

    """
    result = _make_datetime(value)
    if not result.tzinfo:
        raise ValueError(
            f"value was a timestamp, but no timezone was set! "
            f"Value was a '{value.__class__.__name__}' object: {repr(value)}"
            f"\n\n"
            f"Converted to naive 'datetime.datetime' object: {repr(result)}"
        )

    return result


def _make_datetime(value):
    """Helper function for `make_datetime()`.

    Tries to convert the given value to a
    :class:`datetime.datetime`. But, unlike make_datetime(), if no
    timezone is given, makes a naive `datetime.datetime`.

    Strings will be parsed as ISO 8601 timestamps.

    If a number is provided, it will be interpreted as a UNIX
    timestamp, which by definition is UTC.

    If a `dict` is provided, does `datetime.datetime(**value)`.

    If a `tuple` or a `list` is provided, does
    `datetime.datetime(*value)`. Uses the timezone in the tuple or
    list if provided.

    :param value: something to convert
    :type value: str | unicode | float | int | :class:`datetime.datetime` | dict | list | tuple
    :return: the value after conversion
    :rtype: :class:`datetime.datetime`
    :raises: ValueError | TypeError
    """

    if isinstance(value, str):
        try:
            return aniso8601.parse_datetime(value)
        except Exception as e:
            raise ValueError(
                f"Conversion to datetime.datetime failed. Could not "
                f"parse the given string as an ISO 8601 timestamp: "
                f"{repr(value)}\n\n"
                f"{repr(e)}"
            )

    try:
        if isinstance(value, datetime.datetime):
            return value
        elif isinstance(value, dict):
            tzinfo = value.pop('tzinfo', None)
            if tzinfo:
                return tzinfo.localize(datetime.datetime(**value))
            else:
                return datetime.datetime(**value)
        # struct_time does not preserve millisecond accuracy per
        # TinCan spec, so this is disabled to discourage its use.
        # elif isinstance(value, struct_time):
        #     posix = mktime(value)
        #     return datetime.datetime.utcfromtimestamp(posix).replace(tzinfo=utc)
        elif isinstance(value, (tuple, list)):
            return tuple_to_datetime(value)
        else:
            return datetime.datetime.utcfromtimestamp(value).replace(tzinfo=utc)
    except Exception as e:
        msg = (
            f"Could not convert the given value of type '{value.__class__.__name__}' to a "
            f"datetime.datetime: {repr(value)}\n\n"
            f"{repr(e)}"
        )
        raise TypeError(msg) if isinstance(e, TypeError) else ValueError(msg)


def jsonify_datetime(value):
    assert isinstance(value, datetime.datetime)
    return value.isoformat()


def tuple_to_datetime(value):
    # look at the last value and see if it might be a tzinfo
    tzinfo = value[-1]
    tzinfo = tzinfo if hasattr(tzinfo, 'localize') else None

    if tzinfo:
        try:
            args = value[:-1]
            return tzinfo.localize(datetime.datetime(*args))
        except Exception as e:
            raise ValueError(
                f"Failed to call tzinfo.localize(datetime) method "
                f"of tzinfo object: {repr(tzinfo)}\n"
                f"tuple to convert to datetime.datetime was: {repr(value)}"
                f"\n\n"
                f"{repr(e)}"
            )
    else:
        return datetime.datetime(*value)
