# Copyright 2014 Rustici Software
#
# Licensed under the Apache License, Version 2.0 (the "License");
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

from datetime import timedelta

from tincan.serializable_base import SerializableBase
from tincan.score import Score
from tincan.extensions import Extensions
from tincan.conversions.iso8601 import make_timedelta


class Result(SerializableBase):
    """Stores the state of an activity.

    Can be created from a dict, another Result, or from kwargs.

    All these attributes are optional and settable to None:

    :param score: Contains the score and its scaling information
    :type score: :class:`tincan.Score`
    :param success: Whether successful
    :type success: bool
    :param completion: Whether completed
    :type completion: bool
    :param duration: How long it took
    :type duration: timedelta
    :param response: HTTPResponse data
    :type response: unicode
    :param extensions: Custom user data
    :type extensions: :class:`tincan.Extensions`
    """

    _props = [
        'score',
        'success',
        'completion',
        'duration',
        'response',
        'extensions',
    ]

    def __init__(self, *args, **kwargs):
        self._score = None
        self._success = None
        self._completion = None
        self._duration = None
        self._response = None
        self._extensions = None

        super(Result, self).__init__(*args, **kwargs)

    @property
    def score(self):
        """Score for Result

        :setter: Tries to convert to :class:`tincan.Score`. If
        None is provided, this signifies the absence of this data.
        :setter type: :class:`tincan.Score` | dict | None
        :rtype: :class:`tincan.Score` | None

        """
        return self._score

    @score.setter
    def score(self, value):
        try:
            self._score = value if value is None or isinstance(value, Score) else Score(value)
        except Exception as e:
            msg = (
                "Property 'score' in 'tincan.%s' object: could not create a"
                " 'tincan.Score' object from value: %s\n\n" %
                (
                    self.__class__.__name__,
                    repr(value)
                ))
            msg += e.message
            e_type = TypeError if not isinstance(value, dict) else ValueError
            raise e_type(msg)

    @score.deleter
    def score(self):
        del self._score

    @property
    def success(self):
        """Success for Result

        :setter: Tries to convert to bool. If None is provided,
        this signifies the absence of this data.
        :setter type: bool | None
        :rtype: bool | None

        """
        return self._success

    @success.setter
    def success(self, value):
        self._success = value if value is None else bool(value)

    @success.deleter
    def success(self):
        del self._success

    @property
    def completion(self):
        """Completion for Result

        :setter: Tries to convert to bool. If None is provided,
        this signifies the absence of this data.
        :setter type: bool | None
        :rtype: bool | None

        """
        return self._completion

    @completion.setter
    def completion(self, value):
        self._completion = value if value is None else bool(value)

    @completion.deleter
    def completion(self):
        del self._completion

    @property
    def duration(self):
        """Duration for Result

        :setter: Tries to convert to :class:`datetime.timedelta`. If
        None is provided, this signifies the absence of this data.

        Strings will be parsed as ISO 8601 durations.

        If a number is provided, it will be interpreted as the number of
        seconds.

        If a `dict` is provided, does `datetime.timedelta(**value)`.

        :setter type: :class:`datetime.timedelta` | unicode | str | int | float | dict | None
        :rtype: :class:`datetime.timedelta` | None
        :raises: ValueError if the provided data was a valid type, but could not be converted
        :raises: TypeError if unsupported type is provided
        """
        return self._duration

    @duration.setter
    def duration(self, value):
        if value is None or isinstance(value, timedelta):
            self._duration = value
            return

        try:
            self._duration = make_timedelta(value)
        except Exception as e:
            e.message = (
                "Property 'duration' in a 'tincan.%s' object must be set with a "
                "datetime.timedelta, str, unicode, int, float or None.\n\n%s" %
                (
                    self.__class__.__name__,
                    e.message,
                )
            )
            raise e

    @duration.deleter
    def duration(self):
        del self._duration

    @property
    def response(self):
        """Response for Result

        :setter: Tries to convert to unicode. If None is provided,
        this signifies the absence of this data.
        :setter type: unicode | str | None
        :rtype: unicode | None

        """
        return self._response

    @response.setter
    def response(self, value):
        try:
            self._response = value if value is None else str(value)
        except Exception as e:
            e_type = ValueError if isinstance(value, (list, tuple)) else TypeError
            msg = (
                "Property 'response' in a 'tincan.%s' object must be set with a "
                "string, unicode or None.\n\n" %
                self.__class__.__name__,
            )
            msg += e.message
            raise e_type(msg)

    @response.deleter
    def response(self):
        del self._response

    @property
    def extensions(self):
        """Extensions for Result

        :setter: Tries to convert to :class:`tincan.Extensions`. If None is provided,
        this signifies the absence of this data.
        :setter type: :class:`tincan.Extensions` | dict | None
        :rtype: :class:`tincan.Extensions` | None

        """
        return self._extensions

    @extensions.setter
    def extensions(self, value):
        if value is None or isinstance(value, Extensions):
            self._extensions = value
            return
        try:
            self._extensions = Extensions(value)
        except Exception as e:
            msg = (
                "Property 'extensions' in 'tincan.%s' object: could not create a"
                " 'tincan.Extensions' object from value: %s\n\n" %
                (
                    self.__class__.__name__,
                    repr(value)
                ))
            msg += e.message
            e_type = ValueError if isinstance(value, dict) else TypeError
            raise e_type(msg)

    @extensions.deleter
    def extensions(self):
        del self._extensions
