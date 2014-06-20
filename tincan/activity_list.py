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
from tincan.activity import Activity
from tincan.version import Version

"""
.. module:: activity_list
   :synopsis: A wrapper for a list that is able to type check

"""


class ActivityList(list, SerializableBase):

    def __init__(self, *args, **kwargs):
        new_args = [Activity(v) for v in list(*args, **kwargs)]
        super(ActivityList, self).__init__(new_args)

    def __setitem__(self, ind, value):
        if not isinstance(value, Activity):
            value = Activity(value)
        super(ActivityList, self).__setitem__(ind, value)

    def append(self, value):
        if not isinstance(value, Activity):
            value = Activity(value)
        super(ActivityList, self).append(value)

    def extend(self, value):
        new_args = [Activity(v) for v in value]
        super(ActivityList, self).extend(new_args)

    def insert(self, ind, value):
        if not isinstance(value, Activity):
            value = Activity(value)
        super(ActivityList, self).insert(ind, value)

    def _as_version(self, version=Version.latest):
        return [v.as_version(version) for v in self]
