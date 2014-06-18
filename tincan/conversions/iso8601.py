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

"""
Functions for converting ``datetime.timedelta`` and
``datetime.datetime`` to and from ISO 8601 strings.
"""

import datetime
import aniso8601


def make_timedelta(value):
    """Tries to convert the given value to a ``datetime.timedelta``.

    Strings will be parsed as ISO 8601 durations.

    If a number is provided, it will be interpreted as the number of
    seconds.

    If a ``dict`` is provided, does ``datetime.timedelta(**value)``.

    :param value: something to convert
    :type value: str | unicode | float | int | datetime.timedelta | dict
    :return: the value after conversion
    :rtype: datetime.timedelta
    """

    if isinstance(value, datetime.timedelta):
        return value
    elif isinstance(value, basestring):
        try:
            return aniso8601.parse_duration(value)
        except Exception as e:
            msg = (
                "Conversion to datetime.timedelta failed. Could not "
                "parse the given string as an ISO 8601 duration: "
                "%s\n\n"
                "%s" %
                (
                    repr(value),
                    e.message,
                )
            )
            raise ValueError(msg)

    try:
        if isinstance(value, dict):
            return datetime.timedelta(**value)
        else:
            return datetime.timedelta(seconds=value)
    except Exception as e:
        msg = (
            "Could not convert the given value of type '%s' to a "
            "datetime.timedelta: %s\n\n"
            "%s" %
            (
                value.__class__.__name__,
                repr(value),
                e.message,
            )
        )
        raise TypeError(msg) if isinstance(e, TypeError) else ValueError(msg)


def jsonify_timedelta(value):
    """Converts a ``datetime.timedelta`` to an ISO 8601 duration
    string for JSON-ification.

    :param value: something to convert
    :type value: datetime.timedelta
    :return: the value after conversion
    :rtype unicode
    """

    # split seconds to larger units
    seconds = value.total_seconds()
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    days, hours, minutes = map(int, (days, hours, minutes))
    seconds = round(seconds, 6)

    ## build date
    date = ''
    if days:
        date = days + 'D'

    ## build time
    time = u'T'

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
        seconds = '{:02}'.format(seconds)
    else:
        # 9 chars long w/leading 0, 6 digits after decimal
        seconds = '%09.6f' % seconds
    time += '{}S'.format(seconds)

    return u'P' + date + time
