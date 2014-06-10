#!/usr/bin/env python

from tincan.tincanbase import TinCanBaseObject


class Score(TinCanBaseObject):
    """
    Contains the scaled, raw, min and max scores.
    """
    _allowed_properties = [
        'scaled',
        'raw',
        'min',
        'max',
    ]

    def __init__(self, **kwargs):
        """
        :param scaled: scaled score, 0.0-1.0
        :type scaled: float
        :param raw: raw score
        :type raw: float
        :param min: minimum score possible
        :type min: float
        :param max: maximum score possible
        :type max: float
        """
        filtered_keys = [k for k in kwargs if k in self._allowed_properties]
        for k in filtered_keys:
            setattr(self, k, kwargs[k])

    def __eq__(self, other):
        return isinstance(other, Score) and self.__dict__ == other.__dict__
