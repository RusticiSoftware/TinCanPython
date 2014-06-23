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

from tincan.serializable_base import SerializableBase

"""
.. module:: typed_list
   :synopsis: A wrapper for a list that ensures the list consists of only one type

"""


class TypedList(list, SerializableBase):

    _cls = None

    def __init__(self, *args, **kwargs):
        if self._cls is None:
            raise ValueError("_cls has not be set")
        new_args = [self._cls(v) for v in list(*args, **kwargs)]
        super(TypedList, self).__init__(new_args)

    def __setitem__(self, ind, value):
        if self._cls is None:
            raise ValueError("_cls has not be set")
        if not isinstance(value, self._cls):
            value = self._cls(value)
        super(TypedList, self).__setitem__(ind, value)

    def append(self, value):
        if self._cls is None:
            raise ValueError("_cls has not be set")
        if not isinstance(value, self._cls):
            value = self._cls(value)
        super(TypedList, self).append(value)

    def extend(self, value):
        if self._cls is None:
            raise ValueError("_cls has not be set")
        new_args = [self._cls(v) for v in value]
        super(TypedList, self).extend(new_args)

    def insert(self, ind, value):
        if self._cls is None:
            raise ValueError("_cls has not be set")
        if not isinstance(value, self._cls):
            value = self._cls(value)
        super(TypedList, self).insert(ind, value)
