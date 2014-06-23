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

from tincan.serializable_base import SerializableBase
from tincan.score import Score
from tincan.extensions import Extensions
from tincan.version import Version
from tincan.conversions.bytearray import jsonify_bytearray
##TODO: add converters for ISO 8601 duration <-> timedelta
# from tincan.iso8601 import make_timedelta, make_duration

# from datetime import timedelta


class Result(SerializableBase):

    _props = [
        'score',
        'success',
        'completion',
        'duration',
        'response',
        'extensions',
    ]

    @property
    def score(self):
        """Score for Result

		:setter: Tries to convert to Score
		:setter type: :mod:`tincan.score`
		:rtype: :mod:`tincan.score`

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
        """Score for Result

		:setter: Tries to convert to bool
		:setter type: bool
		:rtype: bool

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

		:setter: Tries to convert to bool
		:setter type: bool
		:rtype: bool

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

		:setter: Tries to convert to timdelta
		:setter type: :mod:`datetime.timedelta`
		:rtype: :mod:`datetime.timedelta`

		"""
        return self._duration

    ##TODO: add converters for ISO 8601 duration <-> timedelta
    @duration.setter
    def duration(self, value):
        if value is None or isinstance(value, basestring):
            self._duration = value
            return
        elif not isinstance(value, basestring):
            raise TypeError(
                "Property 'duration' in a 'tincan.%s' object must be set with a "
                "str, unicode, or None." %
                self.__class__.__name__
            )

        self._duration = value if value is None else unicode(value, encoding='utf-8')

    @duration.deleter
    def duration(self):
        del self._duration


    @property
    def response(self):
        """Response for Result

		:setter: Tries to convert to unicode
		:setter type: unicode
		:rtype: unicode

		"""
        return self._response

    @response.setter
    def response(self, value):
        try:
            self._response = value if value is None else unicode(value)
        except Exception as e:
            e_type = ValueError if isinstance(value, (list, tuple)) else TypeError
            msg = (
                "Property 'response' in a 'tincan.%s' object must be set with a "
                "bytestring, string, unicode, list of ints 0-255, or None.\n\n" %
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

		:setter: Tries to convert to Extensions
		:setter type: :mod:`tincan.extensions`
		:rtype: :mod:`tincan.extensions`

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
            e_type = TypeError if not isinstance(value, dict) else ValueError
            raise e_type(msg)

    @extensions.deleter
    def extensions(self):
        del self._extensions

