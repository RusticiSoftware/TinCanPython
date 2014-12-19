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

"""
.. module:: statement_targetable
   :synopsis: Provides a way to define objects as targetable by a statement

   At this time, objects that are targetable need access to only the \
   object type, but this may change in the future

"""


class StatementTargetable(object):
    def __init__(self):
        self.object_type = None

    def get_object_type(self):
        """Returns the object type of self [Activity | Agent | \
        StatementRef | SubStatement]
        """
        return self.object_type
