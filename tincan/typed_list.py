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

from tincan.serializable_base import SerializableBase

"""
.. module:: typed_list
   :synopsis: A wrapper for a list that ensures the list consists of only one type

"""


class TypedList(list, SerializableBase):
    _cls = None

    def __init__(self, *args, **kwargs):
        self._check_cls()
        new_args = [self._make_cls(v) for v in list(*args, **kwargs)]
        super(TypedList, self).__init__(new_args)

    def __setitem__(self, ind, value):
        self._check_cls()
        value = self._make_cls(value)
        super(TypedList, self).__setitem__(ind, value)

    def _check_cls(self):
        """If self._cls is not set, raises ValueError.

        :raises: ValueError
        """
        if self._cls is None:
            raise ValueError("_cls has not been set")

    def _make_cls(self, value):
        """If value is not instance of self._cls, converts and returns
        it. Otherwise, returns value.

        :param value: the thing to make a self._cls from
        :rtype self._cls
        """
        if isinstance(value, self._cls):
            return value
        return self._cls(value)

    def append(self, value):
        self._check_cls()
        value = self._make_cls(value)
        super(TypedList, self).append(value)

    def extend(self, value):
        self._check_cls()
        new_args = [self._make_cls(v) for v in value]
        super(TypedList, self).extend(new_args)

    def insert(self, ind, value):
        self._check_cls()
        value = self._make_cls(value)
        super(TypedList, self).insert(ind, value)
