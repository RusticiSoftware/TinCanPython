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
from tincan.activity_list import ActivityList
from tincan.activity import Activity


class ContextActivities(SerializableBase):
    _props = [
        'category',
        'parent',
        'grouping',
        'other',
    ]

    def __init__(self, *args, **kwargs):
        self._category = None
        self._parent = None
        self._grouping = None
        self._other = None

        super(ContextActivities, self).__init__(*args, **kwargs)

    @property
    def category(self):
        """Category for Context Activities

        :setter: Tries to convert to :class:`tincan.ActivityList`
        :setter type: :class:`tincan.ActivityList`
        :rtype: :class:`tincan.ActivityList`

        """
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
        """Parent for Context Activities

        :setter: Tries to convert to :class:`tincan.ActivityList`
        :setter type: :class:`tincan.ActivityList`
        :rtype: :class:`tincan.ActivityList`

        """
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
        """Grouping for Context Activities

        :setter: Tries to convert to :class:`tincan.ActivityList`
        :setter type: :class:`tincan.ActivityList`
        :rtype: :class:`tincan.ActivityList`

        """
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
        """Other for Context Activities

        :setter: Tries to convert to :class:`tincan.ActivityList`
        :setter type: :class:`tincan.ActivityList`
        :rtype: :class:`tincan.ActivityList`

        """
        return self._other

    @other.setter
    def other(self, value):
        value = self._activity_or_list(value)
        self._other = value

    @other.deleter
    def other(self):
        del self._other

    @staticmethod
    def _activity_or_list(value):
        """Tries to convert value to :class:`tincan.ActivityList`

        :setter type: :class:`tincan.ActivityList`
        :rtype: :class:`tincan.ActivityList`
        """
        result = value
        if value is not None and not isinstance(value, ActivityList):
            try:
                result = ActivityList([Activity(value)])
            except (TypeError, AttributeError):
                result = ActivityList(value)
        return result
