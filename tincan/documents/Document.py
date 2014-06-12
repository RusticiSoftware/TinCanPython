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


class Document(object):

    _properties = [
        "id",
        "content_type",
        "content",
        "etag",
        "time_stamp",
    ]

    def __init__(self, *args, **kwargs):
        """Creates a new Document object, either from a dict, another Document, or from kwargs

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
        #copy construction
        new_kwargs = {}
        for obj in args:
            new_kwargs.update(obj if isinstance(obj, dict) else obj.__dict__)

        if kwargs:
            new_kwargs.update(kwargs)

        filtered_keys = [k for k in new_kwargs.keys() if k in self._properties]
        for k in filtered_keys:
            setattr(self, k, new_kwargs[k])

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        """Setter for the _id attribute

        :param value: Desired value for document's id
        :type value: str
        """
        if not isinstance(value, basestring):
            raise TypeError(
                "Property 'id' in 'tincan.%s' must be set with a basestring." % self.__class__.__name__
            )
        self._id = value

    @id.deleter
    def id(self):
        del self._id

    @property
    def content_type(self):
        return self._content_type

    @content_type.setter
    def content_type(self, value):
        """Setter for the _content_type attribute

        :param value: Desired value for content type of document's content
        :type value: str
        """
        if not isinstance(value, basestring):
            raise TypeError(
                "Property 'content_type' in 'tincan.%s' must be set with a basestring." % self.__class__.__name__
            )
        self._content_type = value

    @content_type.deleter
    def content_type(self):
        del self._content_type

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        """Setter for the _content attribute

        :param value: Desired value for document's content
        :type value: str | bytearray
        """
        if isinstance(value, basestring):
            value = bytearray(value, "utf-8")
        elif not isinstance(value, bytearray):
            raise TypeError(
                "Property 'content' in 'tincan.%s' must be set with a bytearray or basestring." % self.__class__.__name__
            )

        self._content = value

    @content.deleter
    def content(self):
        del self._content

    @property
    def etag(self):
        return self._etag

    @etag.setter
    def etag(self, value):
        """Setter for the _etag attribute

        :param value: Desired value for the document's content
        :type value: str
        """
        if not isinstance(value, basestring):
            raise TypeError(
                "Property 'etag' in 'tincan.%s' must be set with a basestring." % self.__class__.__name__
            )
        self._etag = value

    @etag.deleter
    def etag(self):
        del self._etag

    @property
    def time_stamp(self):
        return self._time_stamp

    @time_stamp.setter
    def time_stamp(self, value):
        """Setter for the _time_stamp attribute

        :param value: Desired value for the document's timestamp
        :type value: datetime | str
        """
        if isinstance(value, datetime.datetime):
            value = value.isoformat()
        elif not isinstance(value, basestring):
            raise TypeError(
                "Property 'time_stamp' in 'tincan.%s' must be set "
                "with a datetime object or basestring." % self.__class__.__name__
            )

        self._time_stamp = value

    @time_stamp.deleter
    def time_stamp(self):
        del self._content_type