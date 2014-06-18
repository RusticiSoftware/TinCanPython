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
Functions for converting data to ``bytearray``s and ``bytearray``s to
JSON-friendly types.
"""


def make_bytearray(value):
    """Tries to convert the given value to a ``bytearray``.

    :param value: something to convert
    :type value: str | unicode | bytearray
    :return: the value after conversion
    :rtype bytearray
    """

    try:
        if isinstance(value, unicode):
            return bytearray(value, 'utf-8')
        else:
            return bytearray(value)
    except Exception as e:
        msg = (
            "Could not convert the given value of type '%s' to "
            "a bytearray: %s" %
            (
                value.__class__.__name__,
                repr(value),
            )
        )
        raise TypeError(msg) if isinstance(e, TypeError) else ValueError(msg)

def jsonify_bytearray(value):
    """Converts a ``bytearray`` to a unicode string for JSON-ification.

    :param value: something to convert
    :type value: bytearray
    :return: the value after conversion
    :rtype unicode
    """

    return value.decode('utf-8')