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

from datetime import timedelta

from tincan.serializable_base import SerializableBase
from tincan.score import Score
from tincan.extensions import Extensions
from tincan.conversions.bytearray import make_bytearray
from tincan.conversions.iso8601 import make_timedelta


class Result(SerializableBase):

    """Stores the state of an activity.

    Can be created from a dict, another Result, or from kwargs.

    :param score: Contains the score and its scaling information
    :type score: Score
    :param success: Whether successful
    :type success: bool
    :param completion: Whether completed
    :type completion: bool
    :param duration: How long it took
    :type duration: timedelta
    :param response: HTTPResponse data
    :type response: bytearray
    :param extensions: Custom user data
    :type extensions: Extensions
    """

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
        return self._score

    @score.setter
    def score(self, value):
        """Setter for the _score attribute. Tries to convert to
        tincan.Score object.

        :param value: The Result's score data.
        :type tincan.Score | dict | None
        """
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
        return self._success

    @success.setter
    def success(self, value):
        """Setter for the _success attribute. Tries to convert to bool.

        :param value: whether the activity was successful
        :type value: bool | None
        """

        self._success = value if value is None else bool(value)

    @success.deleter
    def success(self):
        del self._success


    @property
    def completion(self):
        return self._completion

    @completion.setter
    def completion(self, value):
        """Setter for the _completion attribute. Tries to convert to bool.

        :param value: whether the activity was completed
        :type value: bool | None
        """

        self._completion = value if value is None else bool(value)

    @completion.deleter
    def completion(self):
        del self._completion


    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        """Setter for the _duration attribute. Tries to convert to a
        :class:`datetime.timedelta` object.

        :param value: how long the activity took
        :type value: :class:`datetime.timedelta` | unicode | str | None
        """

        if value is None:
            self._duration = None
        elif isinstance(value, timedelta):
            self._duration = value
        elif isinstance(value, (str, unicode)):
            self._duration = make_timedelta(value)
        elif not isinstance(value, basestring):
            raise TypeError(
                "Property 'duration' in a 'tincan.%s' object must be set with a "
                "str, unicode, or None." %
                self.__class__.__name__
            )

    @duration.deleter
    def duration(self):
        del self._duration


    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, value):
        """Setter for the _response attribute. Tries to convert to
        bytearray.

        :param value: the response data
        :type value: bytearray | str | unicode | None
        """

        try:
            self._response = value if value is None else make_bytearray(value)
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
        return self._extensions

    @extensions.setter
    def extensions(self, value):
        """Setter for the _extensions attribute. Tries to convert to
        tincan.Extensions object.

        :param value: custom additions to TinCan
        :type value: tincan.Extensions | dict | None
        """

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