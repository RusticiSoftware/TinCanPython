#!/usr/bin/env python

from tincan.tincanbase import TinCanBaseObject
from tincan.score import Score
from tincan.extensions import Extensions

class Result(TinCanBaseObject):
    """
    Stores the state of an activity.
    """
    _allowed_properties = [
        'score',
        'success',
        'completion',
        'duration',
        'response',
        'extensions',
    ]

    _nested_objects = {
        'score': Score,
        'extensions': Extensions,
    }

    def __init__(self, **kwargs):
        """
        :param score: Contains the score and its scaling information
        :type score: Score
        :param success: Whether successful
        :type success: bool
        :param completion: Whether completed
        :type completion: bool
        :param duration: How long it took, as an ISO 8601 duration
        :type str
        :param response: HTTPResponse data
        :type bytearray
        :param extensions: Custom user data
        :type extensions: Extensions
        """
        filtered_keys = [k for k in kwargs if k in self._allowed_properties]
        for k in filtered_keys:
            setattr(self, k, kwargs[k])

    def __setattr__(self, attr, value):
        """
        Converts to TinCan objects if possible.
        """
        if attr not in self._allowed_properties:
            raise AttributeError(
                "Attribute '%s' of '%s' object cannot be set" % (attr, self.__class__.__name__))
        elif value is not None and attr in self._nested_objects:
            cls = self._nested_objects[attr]
            self.__dict__[attr] = value if isinstance(value, cls) else cls(**value)
        else:
            self.__dict__[attr] = value

    def __eq__(self, other):
        return isinstance(other, Result) and self.__dict__ == other.__dict__
