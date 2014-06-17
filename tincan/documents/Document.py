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
    :type id: str
    :param content_type: The content_type of the content of this document
    :type content_type: str
    :param content: The content of this document
    :type content: bytearray
    :param etag: The etag of this document
    :type etag: str
    :param time_stamp: The time stamp of this document
    :type time_stamp: str
    """

    _props = [
        'id',
        'content',
        'content_type',
        'etag',
        'time_stamp',
    ]

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        """Setter for the _id attribute. Tries to convert to string.

        :param value: Document's id
        :type value: str
        """
        if not isinstance(value, basestring) and value is not None:
            str(value)
        self._id = value

    @id.deleter
    def id(self):
        del self._id

    @property
    def content_type(self):
        return self._content_type

    @content_type.setter
    def content_type(self, value):
        """Setter for the _content_type attribute. Tries to convert to string.

        :param value: Desired value for content type of document's content
        :type value: str
        """
        if not isinstance(value, basestring) and value is not None:
            str(value)
        self._content_type = value

    @content_type.deleter
    def content_type(self):
        del self._content_type

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        """Setter for the _content attribute. Tries to convert to a bytearray.

        :param value: Desired value for document's content
        :type value: str | bytearray
        """
        if not isinstance(value, bytearray) and value is not None:
            value = bytearray(str(value), "utf-8")

        self._content = value

    @content.deleter
    def content(self):
        del self._content

    @property
    def etag(self):
        return self._etag

    @etag.setter
    def etag(self, value):
        """Setter for the _etag attribute. Tries to convert to string.

        :param value: Desired value for the document's content
        :type value: str
        """
        if not isinstance(value, basestring) and value is not None:
            str(value)
        self._etag = value

    @etag.deleter
    def etag(self):
        del self._etag

    @property
    def time_stamp(self):
        return self._time_stamp

    @time_stamp.setter
    def time_stamp(self, value):
        """Setter for the _time_stamp attribute. Tries to convert to string.

        :param value: Desired value for the document's timestamp
        :type value: datetime | str
        """
        if isinstance(value, datetime.datetime):
            value = value.isoformat()
        elif not isinstance(value, basestring) and value is not None:
            str(value)

        self._time_stamp = value

    @time_stamp.deleter
    def time_stamp(self):
        del self._content_type