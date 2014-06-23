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
        """

        :param usage_type: A URI describing the purpose of the attachment
        :type usage_type: str
        :param display: The human readable name for the attachment
        :type display: :mod:`tincan.languagemap`
        :param description: A plain description of the purpose of the attachment (optional)
        :type description: :mod:`tincan.languagemap`
        :param content_type: The MIME type of the attachment file
        :type content_type: str
        :param length: The size of the attachment in octets
        :type length: int
        :param sha2: The sha2 hash of the contents of the attachment
        :type sha2: str
        :param fileurl: The URL of the file's contents themselves (optional)
        :type fileurl: str

        """

        super(Attachment, self).__init__(*args, **kwargs)

    @property
    def usage_type(self):
        return self._usage_type

    @usage_type.setter
    def usage_type(self, value):
        """Setter for the _usage_type attribute. Tries to convert to string.

        :param value: The attachment's usage_type
        :type value: str

        """
        if value is not None:
            if not isinstance(value, basestring):
                value = str(value)
            elif value == '':
                raise ValueError("Property usage_type cannot be set to an empty string")
        self._usage_type = value
    
    @usage_type.deleter
    def usage_type(self):
        del self._usage_type

    @property
    def content_type(self):
        return self._content_type

    @content_type.setter
    def content_type(self, value):
        """Setter for the _content_type attribute. Tries to convert to string.

        :param value: The attachment's content_type
        :type value: str

        """
        if value is not None:
            if not isinstance(value, basestring):
                value = str(value)
            elif value == '':
                raise ValueError("Property content_type cannot be set to an empty string")
        self._content_type = value

    @content_type.deleter
    def content_type(self):
        del self._content_type

    @property
    def length(self):
        return self._length
    
    @length.setter
    def length(self, value):
        """Setter for the _length attribute. Tries to convert to string.

        :param value: The attachment's length
        :type value: int

        """
        if value is not None:
            if not isinstance(value, (int, long)):
                value = long(value)
        self._length = value
        
    @length.deleter
    def length(self):
        del self._length

    @property
    def sha2(self):
        return self._sha2
    
    @sha2.setter
    def sha2(self, value):
        """Setter for the _sha2 attribute. Tries to convert to string.

        :param value: The attachment's sha2
        :type value: str

        """
        if value is not None:
            if not isinstance(value, basestring):
                value = str(value)
            elif value == '':
                raise ValueError("Property sha2 cannot be set to an empty string")
        self._sha2 = value
        
    @sha2.deleter
    def sha2(self):
        del self._sha2
        
    @property
    def fileurl(self):
        return self._fileurl

    @fileurl.setter
    def fileurl(self, value):
        """Setter for the _fileurl attribute. Tries to convert to string.

        :param value: The attachment's fileurl
        :type value: str

        """
        if value is not None:
            if not isinstance(value, basestring):
                value = str(value)
            elif value == '':
                raise ValueError("Property fileurl cannot be set to an empty string")
        self._fileurl = value

    @fileurl.deleter
    def fileurl(self):
        del self._fileurl

    @property
    def display(self):
        return self._display

    @display.setter
    def display(self, value):
        """Setter for the _display attribute. Tries to convert to :mod:`tincan.LanguageMap`

        :param value: The attachment's display
        :type value: :mod:`tincan.LanguageMap`

        """
        if value is not None:
            if not value:
                value = None
            elif not isinstance(value, LanguageMap):
                value = LanguageMap(value)
            elif len(value) == 0:
                value = None
        self._display = value

    @display.deleter
    def display(self):
        del self._display

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        """Setter for the _description attribute. Tries to convert to :mod:`tincan.LanguageMap`

        :param value: The attachment's description
        :type value: :mod:`tincan.LanguageMap`

        """
        if value is not None:
            if not value:
                value = None
            elif not isinstance(value, LanguageMap):
                value = LanguageMap(value)
            elif len(value) == 0:
                value = None
        self._description = value

    @description.deleter
    def description(self):
        del self._description