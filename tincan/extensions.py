#!/usr/bin/env python

from tincan.tincanbase import TinCanBaseObject


class Extensions(TinCanBaseObject, dict):
    """
    Contains domain-specific custom data.

    Use this like a regular Python dict.
    """
    def __init__(self, *args, **kwargs):
        super(Extensions, self).__init__(*args, **kwargs)
