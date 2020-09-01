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
from tincan.base import Base


class HTTPRequest(Base):
    """Creates a new HTTPRequest object, either from a dict, another object, or from kwargs

    :param method: Method for the HTTP connection ("GET", "POST", "DELETE", etc.)
    :type method: unicode
    :param resource: Resource for the LRS HTTP connection ("about", "statements", "activities/state", etc.)
    :type resource: unicode
    :param headers: Headers for the HTTP connection ("If-Match", "Content-Type", etc.)
    :type headers: dict(unicode:unicode)
    :param query_params: Query parameters for the HTTP connection ("registration", "since", "statementId", etc.)
    :type query_params: dict(unicode:unicode)
    :param content: Content body for the HTTP connection. Valid json string.
    :type content: unicode
    :param ignore404: True if this request should consider a 404 response successful, False otherwise
    :type ignore404: bool
    """

    _props_req = [
        'method',
        'resource',
        'headers',
        'query_params',
    ]

    _props = [
        'content',
        'ignore404',
    ]

    _props.extend(_props_req)

    def __init__(self, *args, **kwargs):
        self._method = None
        self._resource = None
        self._headers = None
        self._query_params = None
        self._content = None
        self._ignore404 = None

        super(HTTPRequest, self).__init__(*args, **kwargs)

    @property
    def method(self):
        """Method for the HTTP connection ("GET", "POST", "DELETE", etc.)

        :setter: Tries to convert to unicode
        :setter type: str | unicode
        :rtype: unicode
        """
        return self._method

    @method.setter
    def method(self, value):
        if not isinstance(value, str) and value is not None:
            str(value)
        self._method = value

    @property
    def resource(self):
        """Resource for the LRS HTTP connection ("about", "statements", "activities/state", etc.)

        :setter: Tries to convert to unicode
        :setter type: str | unicode
        :rtype: unicode
        """
        return self._resource

    @resource.setter
    def resource(self, value):
        if not isinstance(value, str) and value is not None:
            str(value)
        self._resource = value

    @property
    def headers(self):
        """Headers for the HTTP connection ("If-Match", "Content-Type", etc.)

        :setter: Accepts a dict or an object
        :setter type: dict
        :rtype: dict
        """
        return self._headers

    @headers.setter
    def headers(self, value):
        val_dict = {}
        if value is not None:
            val_dict.update(value if isinstance(value, dict) else vars(value))
        self._headers = val_dict

    @property
    def query_params(self):
        """Query parameters for the HTTP connection ("registration", "since", "statementId", etc.)

        :setter: Accepts a dict or an object
        :setter type: dict
        :rtype: dict
        """
        return self._query_params

    @query_params.setter
    def query_params(self, value):
        val_dict = {}
        if value is not None:
            val_dict.update(value if isinstance(value, dict) else vars(value))
        self._query_params = val_dict

    @property
    def content(self):
        """Content body for the HTTP connection. Valid json string.

        :setter: Tries to convert to unicode
        :setter type: str | unicode
        :rtype: unicode
        """
        return self._content

    @content.setter
    def content(self, value):
        if not isinstance(value, str) and value is not None:
            value = value.decode("utf-8")
        self._content = value

    @content.deleter
    def content(self):
        del self._content

    @property
    def ignore404(self):
        """True if this request should consider a 404 response successful, False otherwise

        :setter: Tries to convert to boolean
        :setter type: bool
        :rtype: bool
        """
        return self._ignore404

    @ignore404.setter
    def ignore404(self, value):
        self._ignore404 = bool(value)

    @ignore404.deleter
    def ignore404(self):
        del self._ignore404
