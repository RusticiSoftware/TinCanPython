#!/usr/bin/env python

from tincan.tincanbase import TinCanBaseObject


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

    def __init__(self, **kwargs):
        """
        :param score: Contains the score and its scaling information
        :type score: Score
        :param success: Whether successful
        :type success: bool
        :param completion: Whether completed
        :type completion: bool
        :param duration: How long it took
        :param response: HTTPResponse data
        :param extensions: Custom user data
        :type extensions: Extensions
        """
        filtered_keys = [k for k in kwargs.keys() if k in self._allowed_properties]
        for k in filtered_keys:
            setattr(self, k, kwargs[k])
