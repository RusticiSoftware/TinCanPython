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

from http.client import HTTPResponse

from tincan.http_request import HTTPRequest
from tincan.base import Base


class LRSResponse(Base):
    """Creates a new LRSResponse object, either from a dict, another object, or from kwargs

    :param success: True if the LRS return a successful status (sometimes includes 404), False otherwise
    :type success: bool
    :param request: HTTPRequest object that was sent to the LRS
    :type request: HTTPRequest
    :param response: HTTPResponse object that was received from the LRS
    :type response: HTTPResponse
    :param data: Body of the HTTPResponse
    :type data: unicode
    :param content: Parsed content received from the LRS
    """

    _props_req = [
        'success',
        'request',
        'response',
        'data',
    ]

    _props = [
        'content',
    ]

    _props.extend(_props_req)

    def __init__(self, *args, **kwargs):
        self._success = None
        self._request = None
        self._response = None
        self._data = None
        self._content = None

        super(LRSResponse, self).__init__(*args, **kwargs)

    @property
    def success(self):
        """The LRSResponse's success. True if the LRS return a
        successful status (sometimes includes 404), False otherwise.

        :setter: Tries to convert to boolean
        :setter type: bool
        :rtype: bool
        """
        return self._success

    @success.setter
    def success(self, value):
        self._success = bool(value)

    @property
    def request(self):
        """The HTTPRequest object that was sent to the LRS

        :setter: Tries to convert to an HTTPRequest object
        :setter type: :class:`tincan.http_request.HTTPRequest`
        :rtype: :class:`tincan.http_request.HTTPRequest`
        """
        return self._request

    @request.setter
    def request(self, value):
        if value is not None and not isinstance(value, HTTPRequest):
            value = HTTPRequest(value)

        self._request = value

    @property
    def response(self):
        """The HTTPResponse object that was sent to the LRS

        :setter: Must be an HTTPResponse object
        :setter type: :class:`httplib.HTTPResponse`
        :rtype: :class:`httplib.HTTPResponse`
        """
        return self._response

    @response.setter
    def response(self, value):
        if value is not None and not isinstance(value, HTTPResponse):
            raise TypeError(
                f"Property 'response' in 'tincan.{self.__class__.__name__}' must be set with an HTTPResponse object"
            )
        self._response = value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        """Setter for the _data attribute. Should be set from response.read()

        :param value: The body of the response object for the LRSResponse
        :type value: unicode
        """
        if value is not None and isinstance(value, (bytes, bytearray)):
            value = value.decode('utf-8')
        self._data = value

    @property
    def content(self):
        """Parsed content received from the LRS
        """
        return self._content

    @content.setter
    def content(self, value):
        self._content = value

    @content.deleter
    def content(self):
        del self._content
