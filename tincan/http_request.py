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

class HTTPRequest(object):
    def __init__(self, endpoint=None, method=None, resource=None, headers=None,
                 query_params=None, content=None, ignore404=False):
        self.endpoint = endpoint
        self.method = method
        self.resource = resource
        self.content = content
        self.ignore404 = ignore404

        if headers is None:
            self.headers = {}
        else:
            self.headers = headers

        if query_params is None:
            self.query_params = {}
        else:
            self.query_params = query_params