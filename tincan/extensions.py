#!/usr/bin/env python

from tincan.serializable_base import SerializableBase
from tincan.version import Version


class Extensions(dict, SerializableBase):
    """
    Contains domain-specific custom data.

    Use this like a regular Python dict.
    """
    def __init__(self, *args, **kwargs):
        super(Extensions, self).__init__(*args, **kwargs)

    def _as_version(self, version=Version.latest):
        return dict(self)
