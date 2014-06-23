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
#from tincan.activity_list import ActivityList
from tincan.activity import Activity
from tincan.version import Version


class ContextActivities(SerializableBase):

    _props = [
        'category',
        'parent',
        'grouping',
        'other',
    ]

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        value = self._activity_or_list(value)
        self._category = value

    @category.deleter
    def category(self):
        del self._category

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        value = self._activity_or_list(value)
        self._parent = value

    @parent.deleter
    def parent(self):
        del self._parent

    @property
    def grouping(self):
        return self._grouping

    @grouping.setter
    def grouping(self, value):
        value = self._activity_or_list(value)
        self._grouping = value

    @grouping.deleter
    def grouping(self):
        del self._grouping

    @property
    def other(self):
        return self._other

    @other.setter
    def other(self, value):
        value = self._activity_or_list(value)
        self._other = value

    @other.deleter
    def other(self):
        del self._other

    def _activity_or_list(self, value):
        result = value
        if value is not None and not isinstance(value, Activity) and not isinstance(value, ActivityList):
            try:
                result = Activity(value)
            except (TypeError, AttributeError):
                result = ActivityList(value)

        if isinstance(result, Activity):
            result = ActivityList([result])

        return result
