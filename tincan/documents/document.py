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
import datetime
from tincan.base import Base


class Document(Base):
    """Document class can be instantiated from a dict, another Document, or from kwargs

    :param id: The id of this document
    :type id: unicode
    :param content_type: The content type of the content of this document
    :type content_type: unicode
    :param content: The content of this document
    :type content: bytearray
    :param etag: The etag of this document
    :type etag: unicode
    :param time_stamp: The time stamp of this document
    :type time_stamp: unicode
    """
    _props_req = [
        'id',
        'content',
        'content_type',
        'etag',
        'time_stamp',
    ]

    _props = []

    _props.extend(_props_req)

    @property
    def id(self):
        """The Document id

        :setter: Tries to convert to unicode
        :setter type: str | unicode
        :rtype: unicode
        """
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, unicode) and value is not None:
            unicode(value)
        self._id = value

    @property
    def content_type(self):
        """The Document content type

        :setter: Tries to convert to unicode
        :setter type: str | unicode
        :rtype: unicode
        """
        return self._content_type

    @content_type.setter
    def content_type(self, value):
        if not isinstance(value, unicode) and value is not None:
            unicode(value)
        self._content_type = value

    @property
    def content(self):
        """The Document content

        :setter: Tries to convert to bytearray.
        :setter type: str | unicode | bytearray
        :rtype: bytearray
        """
        return self._content

    @content.setter
    def content(self, value):
        if not isinstance(value, bytearray) and value is not None:
            value = bytearray(unicode(value), "utf-8")

        self._content = value

    @property
    def etag(self):
        """The Document etag

        :setter: Tries to convert to unicode
        :setter type: str | unicode
        :rtype: unicode
        """
        return self._etag

    @etag.setter
    def etag(self, value):
        if not isinstance(value, unicode) and value is not None:
            unicode(value)
        self._etag = value

    @property
    def time_stamp(self):
        """The Document time stamp

        :setter: Tries to convert to unicode
        :setter type: str | unicode | :class:`datetime.datetime`
        :rtype: unicode
        """
        return self._time_stamp

    @time_stamp.setter
    def time_stamp(self, value):
        if isinstance(value, datetime.datetime):
            value = value.isoformat()

        if not isinstance(value, unicode) and value is not None:
            unicode(value)

        self._time_stamp = value
