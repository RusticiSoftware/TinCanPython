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

    def __init__(self, *args, **kwargs):
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
        # Copy construction
        if args and len(args) == 1:
            obj = args[0]

            # Copy properties from obj
            new_kwargs = obj if isinstance(obj, dict) else obj.__dict__

            # make kwargs overwrite fields of copied object
            if kwargs:
                new_kwargs.update(kwargs)
            kwargs = new_kwargs

        # Only use the properties in self._allowed_properties
        filtered_keys = [k for k in kwargs if k in self._allowed_properties]
        for k in filtered_keys:
            setattr(self, k, kwargs[k])

    def __eq__(self, other):
        return isinstance(other, Score) and self.__dict__ == other.__dict__
