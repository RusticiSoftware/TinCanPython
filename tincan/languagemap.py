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

from serializablebase import SerializableBase
from version import Version

"""
.. module:: languagemap
   :synopsis: A simple wrapper for a map containing language mappings

"""


class LanguageMap(dict, SerializableBase):

    def __init__(self, *args, **kwargs):
        """Initializes a LanguageMap with the given mapping

        This constructor takes in two arguments, but will only acknowledge one.
        The kwargs parameter is to support the from_json method, and the
        unpacking (**) operator. If the 'map' argument is specified, kwargs
        will be ignored.

        :param map: The intended language mapping
        :type map: dict, LanguageMap

        :raises: LanguageMapTypeError

        """
        check_args = dict(*args, **kwargs)
        map(lambda(k,v): (k, self.check_basestring(v)), check_args.iteritems())
        super(LanguageMap, self).__init__(check_args)

    def __setitem__(self, prop, value):
        """Allows bracket notation for setting values with hyphenated keys

        :param prop: The property to set
        :type prop: str
        :param value: The value to set
        :type value: obj

        :raises: NameError, LanguageMapTypeError

        """
        self.check_basestring(value)
        super(LanguageMap, self).__setitem__(prop, value)

    def _as_version(self, version=Version.latest):
        """Overrides :mod:`base`.as_version. Returns a dict that represents
        the LanugageMap

        :param version: the desired target version for the LanguageMap
        :type version: str

        """
        return dict(self)

    def check_basestring(self, value):
        """Ensures that value is an instance of basestring

        :param value: the value to check
        :type value: any

        """
        if not isinstance(value, basestring):
            raise TypeError("Value must be of type basestring")
