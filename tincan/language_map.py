# Copyright 2014 Rustici Software
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

from tincan.serializable_base import SerializableBase

"""
.. module:: languagemap
   :synopsis: A simple wrapper for a map containing language mappings

"""


class LanguageMap(dict, SerializableBase):
    def __init__(self, *args, **kwargs):
        """Initializes a LanguageMap with the given mapping

        This constructor will first check the arguments for flatness
        to avoid nested languagemaps (which are invalid) and then
        call the base dict constructor

        """
        check_args = dict(*args, **kwargs)
        list(map(lambda k_v: (k_v[0], self._check_basestring(k_v[1])), iter(check_args.items())))
        super(LanguageMap, self).__init__(check_args)

    def __setitem__(self, prop, value):
        """Allows bracket notation for setting values with hyphenated keys

        :param prop: The property to set
        :type prop: str
        :param value: The value to set
        :type value: obj

        :raises: NameError, LanguageMapTypeError

        """
        self._check_basestring(value)
        super(LanguageMap, self).__setitem__(prop, value)

    @staticmethod
    def _check_basestring(value):
        """Ensures that value is an instance of basestring

        :param value: the value to check
        :type value: any

        """
        if not isinstance(value, str):
            raise TypeError("Value must be a stringstring_types")
