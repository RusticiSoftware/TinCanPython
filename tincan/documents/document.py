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
import datetime

from tincan.base import Base
from tincan.conversions.iso8601 import make_datetime


class Document(Base):
    """Document class can be instantiated from a dict, another :class:`tincan.Document`, or from kwargs

    :param id: The id of this document
    :type id: unicode
    :param content_type: The content type of the content of this document
    :type content_type: unicode
    :param content: The content of this document
    :type content: bytearray
    :param etag: The etag of this document
    :type etag: unicode
    :param timestamp: The timestamp of this document
    :type timestamp: :class:`datetime.datetime`

    """
    _props_req = [
        'id',
        'content',
        'content_type',
        'etag',
        'timestamp',
    ]

    _props = []

    _props.extend(_props_req)

    def __init__(self, *args, **kwargs):
        self._id = None
        self._content = None
        self._content_type = None
        self._etag = None
        self._timestamp = None

        super(Document, self).__init__(*args, **kwargs)

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
        if isinstance(value, (bytes, bytearray)) and value is not None:
            value = value.decode("utf-8")
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
        if isinstance(value, (bytes, bytearray)) and value is not None:
            value = value.decode("utf-8")
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
            value = bytearray(value, "utf-8")

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
        if isinstance(value, (bytes, bytearray)) and value is not None:
            value = value.decode("utf-8")
        self._etag = value

    @property
    def timestamp(self):
        """The Document timestamp.

        :setter: Tries to convert to :class:`datetime.datetime`. If
        no timezone is given, makes a naive `datetime.datetime`.

        Strings will be parsed as ISO 8601 timestamps.

        If a number is provided, it will be interpreted as a UNIX
        timestamp, which by definition is UTC.

        If a `dict` is provided, does `datetime.datetime(**value)`.

        If a `tuple` or a `list` is provided, does
        `datetime.datetime(*value)`. Uses the timezone in the tuple or
        list if provided.

        :setter type: :class:`datetime.datetime` | unicode | str | int | float | dict | tuple | None
        :rtype: :class:`datetime.datetime`

        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        if value is None:
            self._timestamp = value
            return

        try:
            self._timestamp = make_datetime(value)
        except TypeError as e:
            message = (
                f"Property 'timestamp' in a 'tincan.{self.__class__.__name__}' "
                f"object must be set with a "
                f"datetime.datetime, str, unicode, int, float, dict "
                f"or None.\n\n{repr(e)}"
            )
            raise TypeError(message) from e
