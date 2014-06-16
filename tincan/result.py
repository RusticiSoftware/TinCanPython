#!/usr/bin/env python

from tincan.serializable_base import SerializableBase
from tincan.score import Score
from tincan.extensions import Extensions
from tincan.version import Version
from tincan.conversions.bytearray import make_bytearray
##TODO: add converters for ISO 8601 duration <-> timedelta
# from tincan.iso8601 import make_timedelta, make_duration

# from datetime import timedelta


class Result(SerializableBase):

    """Stores the state of an activity.

    Can be created from a dict, another Result, or from kwargs.

    :param score: Contains the score and its scaling information
    :type score: Score
    :param success: Whether successful
    :type success: bool
    :param completion: Whether completed
    :type completion: bool
        ##TODO: add converters for ISO 8601 duration <-> timedelta
    :param duration: How long it took
    :type duration: basestring
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
        """Setter for the _score attribute. Tries to convert to Score object.

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
        self._success = value if value is None else bool(value)

    @success.deleter
    def success(self):
        del self._success


    @property
    def completion(self):
        return self._completion

    @completion.setter
    def completion(self, value):
        self._completion = value if value is None else bool(value)

    @completion.deleter
    def completion(self):
        del self._completion


    @property
    def duration(self):
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
        return self._response

    @response.setter
    def response(self, value):
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


    def _as_version(self, version=Version.latest):
        """
        Creates a ``dict`` version of self ready for ``to_json()``.

        :param version: A version specifier, eg. "1.0.1"
        :type version: str
        :return: A new ``dict`` object ready for ``to_json()`` to
        serialize.
        """
        result = {k[1:] if k.startswith('_') else k: v for k, v in vars(self).iteritems()}

        # Perform the out-conversion on attributes that need it
        for attr, value in result.iteritems():
            if value is None or attr not in self._props:
                del result[attr]
            elif isinstance(value, SerializableBase):
                result[attr] = value.as_version(version)
            elif isinstance(value, bytearray):
                result[attr] = jsonify_bytearray(value)

        return result

