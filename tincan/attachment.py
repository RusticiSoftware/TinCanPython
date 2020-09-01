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
from tincan.language_map import LanguageMap

"""
.. module:: Attachment
   :synopsis: An Attachment object that contains an attached file and its information

"""


class Attachment(SerializableBase):
    _props_req = [
        "usage_type",
        "display",
        "content_type",
        "length",
        "sha2"
    ]

    _props = [
        "description",
        "fileurl"
    ]

    _props.extend(_props_req)

    def __init__(self, *args, **kwargs):
        self._usage_type = None
        self._display = None
        self._content_type = None
        self._length = None
        self._sha2 = None
        self._description = None
        self._fileurl = None

        super(Attachment, self).__init__(*args, **kwargs)

    @property
    def usage_type(self):
        """Usage type for Attachment

        :setter: Tries to convert to unicode
        :setter type: unicode
        :rtype: unicode

        """
        return self._usage_type

    @usage_type.setter
    def usage_type(self, value):
        if value is not None:
            if value == '':
                raise ValueError("Property usage_type can not be set to an empty string")
            elif not isinstance(value, str):
                value = str(value)
        self._usage_type = value

    @usage_type.deleter
    def usage_type(self):
        del self._usage_type

    @property
    def content_type(self):
        """Content type for Attachment

        :setter: Tries to convert to unicode
        :setter type: unicode
        :rtype: unicode

        """
        return self._content_type

    @content_type.setter
    def content_type(self, value):
        if value is not None:
            if value == '':
                raise ValueError("Property content_type can not be set to an empty string")
            elif not isinstance(value, str):
                value = str(value)
        self._content_type = value

    @content_type.deleter
    def content_type(self):
        del self._content_type

    @property
    def length(self):
        """Usage type for Attachment

        :setter: Tries to convert to long
        :setter type: int | long
        :rtype: long

        """
        return self._length

    @length.setter
    def length(self, value):
        if value is not None:
            if not isinstance(value, int):
                value = int(value)
        self._length = value

    @length.deleter
    def length(self):
        del self._length

    @property
    def sha2(self):
        """Sha2 for Attachment

        :setter: Tries to convert to unicode
        :setter type: unicode
        :rtype: unicode

        """
        return self._sha2

    @sha2.setter
    def sha2(self, value):
        if value is not None:
            if value == '':
                raise ValueError("Property sha2 can not be set to an empty string")
            elif not isinstance(value, str):
                value = str(value)
        self._sha2 = value

    @sha2.deleter
    def sha2(self):
        del self._sha2

    @property
    def fileurl(self):
        """File URL for Attachment

        :setter: Tries to convert to unicode
        :setter type: unicode
        :rtype: unicode

        """
        return self._fileurl

    @fileurl.setter
    def fileurl(self, value):
        if value is not None:
            if value == '':
                raise ValueError("Property fileurl can not be set to an empty string")
            elif not isinstance(value, str):
                value = str(value)
        self._fileurl = value

    @fileurl.deleter
    def fileurl(self):
        del self._fileurl

    @property
    def display(self):
        """Display for Attachment

        :setter: Tries to convert to :class:`tincan.LanguageMap`
        :setter type: :class:`tincan.LanguageMap`
        :rtype: :class:`tincan.LanguageMap`

        """
        return self._display

    @display.setter
    def display(self, value):
        if value is not None and not isinstance(value, LanguageMap):
            value = LanguageMap(value)
        self._display = value

    @display.deleter
    def display(self):
        del self._display

    @property
    def description(self):
        """Description for Attachment

        :setter: Tries to convert to :class:`tincan.LanguageMap`
        :setter type: :class:`tincan.LanguageMap`
        :rtype: :class:`tincan.LanguageMap`

        """
        return self._description

    @description.setter
    def description(self, value):
        if value is not None and not isinstance(value, LanguageMap):
            value = LanguageMap(value)
        self._description = value

    @description.deleter
    def description(self):
        del self._description
