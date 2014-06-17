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

from tincan.base import Base


class HTTPRequest(Base):
    """Creates a new HTTPRequest object, either from a dict, another object, or from kwargs

    :param endpoint: The remote lrs endpoint used the HTTP connection
    :type endpoint: str
    :param method: Method for the HTTP connection ("GET", "POST", "DELETE", etc.)
    :type method: str
    :param resource: Resource for the LRS HTTP connection ("about", "statements", "activities/state", etc.)
    :type resource: str
    :param headers: Headers for the HTTP connection ("If-Match", "Content-Type", etc.)
    :type headers: dict(str:str)
    :param query_params: Query parameters for the HTTP connection ("registration", "since", "statementId", etc.)
    :type query_params: dict(str:str)
    :param content: Content body for the HTTP connection. Valid json string.
    :type content: str
    :param ignore404: True if this request should consider a 404 response successful, False otherwise
    :type ignore404: bool
    """

    _props_req = [
        "method",
        "resource",
        "headers",
        "query_params",
    ]

    _props = [
        "endpoint",
        "content",
        "ignore404",
    ]

    _props.extend(_props_req)
    
    @property
    def endpoint(self):
        return self._endpoint

    @endpoint.setter
    def endpoint(self, value):
        """Setter for the _endpoint attribute. Tries to convert to string.

        :param value: The request's endpoint
        :type value: str
        """
        if not isinstance(value, basestring) and value is not None:
            str(value)
        self._endpoint = value

    @endpoint.deleter
    def endpoint(self):
        del self._endpoint

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, value):
        """Setter for the _method attribute. Tries to convert to string.
        
        :param value: The request's method
        :type value: str
        """
        if not isinstance(value, basestring) and value is not None:
            str(value)
        self._method = value

    @property
    def resource(self):
        return self._resource

    @resource.setter
    def resource(self, value):
        """Setter for the _resource attribute. Tries to convert to string.
        
        :param value: The request's resource
        :type value: str
        """
        if not isinstance(value, basestring) and value is not None:
            str(value)
        self._resource = value
        
    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, value):
        """Setter for the _headers attribute.

        :param value: The request's headers
        :type value: dict
        """
        val_dict = {}
        if value is not None:
            val_dict.update(value if isinstance(value, dict) else vars(value))
        self._headers = val_dict

    @property
    def query_params(self):
        return self._query_params

    @query_params.setter
    def query_params(self, value):
        """Setter for the _query_params attribute.

        :param value: The request's query parameters
        :type value: dict
        """
        val_dict = {}
        if value is not None:
            val_dict.update(value if isinstance(value, dict) else vars(value))
        self._query_params = val_dict
        
    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        """Setter for the _content attribute. Tries to convert to string.

        :param value: The request's content
        :type value: str
        """
        if not isinstance(value, basestring) and value is not None:
            value = str(value)
        self._content = value

    @content.deleter
    def content(self):
        del self._content
        
    @property
    def ignore404(self):
        return self._ignore404

    @ignore404.setter
    def ignore404(self, value):
        """Setter for the _ignore404 attribute. Tries to convert to bool.

        :param value: If true, this request treats 404 statuses as successful
        :type value: bool
        """
        self._ignore404 = bool(value)

    @ignore404.deleter
    def ignore404(self):
        del self._ignore404