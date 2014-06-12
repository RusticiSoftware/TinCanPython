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

from tincanbase import TinCanBaseObject

"""
.. module:: languagemap
   :synopsis: A simple wrapper for a map containing language mappings

"""


class LanguageMapTypeError(Exception):
    pass


class LanguageMap(TinCanBaseObject):

    def __init__(self, map=None, **kwargs):
        """Initializes a LanguageMap with the given mapping

        This constructor takes in two arguments, but will only acknowledge one.
        The kwargs parameter is to support the from_json method, and the \
        unpacking (**) operator. If the 'map' argument is specified, kwargs \
        will be ignored.

        :param map: The intended language mapping
        :type map: dict, LanguageMap

        :raises: LanguageMapTypeError

        """
        self.set_mapping(map)
        if map is None and kwargs:
            self.set_mapping(kwargs)

    def __repr__(self):
        return '%s' % self.__dict__

    def __getitem__(self, prop):
        """Allows bracket notation for retrieving values with hyphenated keys

        :param prop: The property to return
        :type prop: str

        :raises: AttributeError

        """
        return getattr(self, prop)

    def __setitem__(self, prop, value):
        """Allows bracket notation for setting values with hyphenated keys

        :param prop: The property to set
        :type prop: str
        :param value: The value to set
        :type value: obj

        :raises: NameError, LanguageMapTypeError

        """
        if isinstance(value, basestring):
            setattr(self, prop, value)
        else:
            raise LanguageMapTypeError("Value must be of type string")

    def set_mapping(self, map):
        """Provides error checking when setting the mapping

        :param map: The map that contains the desired keys and values
        :type map: dict, LanguageMap

        :raises: LanguageMapTypeError

        """
        if map is not None:
            new_map = {}
            if isinstance(map, dict):
                for k, v in map.iteritems():
                    if not isinstance(v, basestring):
                        raise LanguageMapTypeError("Mapping may not contain nested objects or None")
                    new_map[k] = v
            elif isinstance(map, LanguageMap):
                for k, v in vars(map).iteritems():
                    if not isinstance(v, basestring):
                        raise LanguageMapTypeError("Mapping may not contain nested objects or None")
                    new_map[k] = v
            else:
                raise LanguageMapTypeError("Arguments cannot be coerced into a LanguageMap")

            self.__dict__ = new_map

    def get_mapping(self):
        """Retrieve the mapping

        .. note:: calling this method is identical to calling vars(languagemap_inst)
        """
        return self.__dict__
