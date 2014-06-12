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

class LRSResponse(object):
    """
    Defines the LRSResponse class which is received from LRS communication.
    """
    def __init__(self, success, request, response, data=None):
        self.success = success
        self.request = request
        self.response = response
        if data is not None:
            for k, v in data:
                setattr(self, k, v)

    def load(self, data):
        for k, v in data:
            setattr(self, k, v)