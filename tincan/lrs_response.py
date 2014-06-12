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

class LRSResponse(object):
    """
    Defines the LRSResponse class which is received from LRS communication.
    """
    _required_properties = [
        "success",
        "request",
        "response",
    ]

    _properties = [
        "content",
    ]

    _properties.extend(_required_properties)


    def __init__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        for k in self._required_properties:
            setattr(self, k, None)

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
    def success(self):
        return self._success

    @success.setter
    def success(self, value):
        """Setter for the _success attribute

        :param value: Desired value for the object's success
        :type value: bool
        """
        if value is not None and not isinstance(value, bool):
            raise TypeError(
                "Property 'success' in 'tincan.%s' must be set with a boolean." % self.__class__.__name__
            )
        self._success = value

    @success.deleter
    def success(self):
        del self._success

    @property
    def request(self):
        return self._request

    @request.setter
    def request(self, value):
        """Setter for the _request attribute

        :param value: Desired object for the response's request attribute
        :type value: HTTPRequest
        """
        if value is not None and not isinstance(value, HTTPRequest):
            raise TypeError(
                "Property 'request' in 'tincan.%s' must be set with an HTTPRequest object" % self.__class__.__name__
            )
        self._request = value

    @request.deleter
    def request(self):
        del self._request

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, value):
        """Setter for the _response attribute

        :param value: Desired object for the response's response attribute
        :type value: HTTPResponse
        """
        if value is not None and not isinstance(value, HTTPResponse):
            raise TypeError(
                "Property 'response' in 'tincan.%s' must be set with an HTTPResponse object" % self.__class__.__name__
            )
        self._response = value

    @response.deleter
    def response(self):
        del self._response

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