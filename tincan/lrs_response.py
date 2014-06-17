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
from httplib import HTTPResponse

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
    :type data: str
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

    @property
    def success(self):
        return self._success

    @success.setter
    def success(self, value):
        """Setter for the _success attribute. Tries to convert to bool.

        :param value: The LRSResponse's success
        :type value: bool
        """
        self._success = bool(value)

    @property
    def request(self):
        return self._request

    @request.setter
    def request(self, value):
        """Setter for the _request attribute. Tries to convert to an HTTPRequest object.

        :param value: The LRSResponse's request attribute
        :type value: HTTPRequest
        """
        if value is not None and not isinstance(value, HTTPRequest):
            value = HTTPRequest(value)

        self._request = value

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, value):
        """Setter for the _response attribute. Must be set with None or an HTTPResponse object.

        :param value: The LRSResponse's response attribute
        :type value: HTTPResponse
        """
        if value is not None and not isinstance(value, HTTPResponse):
            raise TypeError(
                "Property 'response' in 'tincan.%s' must be set with an HTTPResponse object" % self.__class__.__name__
            )
        self._response = value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        """Setter for the _data attribute. Should be set from response.read()

        :param value: The body of the response object for the LRSResponse
        :type value: str
        """
        if value is not None and not isinstance(value, basestring):
            str(value)
        self._data = value

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        """Setter for the _content attribute

        :param value: Desired content for response
        """
        self._content = value

    @content.deleter
    def content(self):
        del self._content