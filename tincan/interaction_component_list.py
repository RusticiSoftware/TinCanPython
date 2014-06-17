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
#    limitations under the License.""

from serializable_base import SerializableBase
from interaction_component import InteractionComponent
from version import Version

"""
.. module:: interactioncomponentlist
   :synopsis: A wrapper for list that is able to type check

"""


class InteractionComponentList(list, SerializableBase):

    def __init__(self, *args, **kwargs):
        """Initializes an InteractionComponentList with the given arguments

        The first step of constructing the list is checking that the
        arguments are of proper type. Once that is done, the base list
        constructor is called.

        """
        check_args = list(*args, **kwargs)
        new_args = []
        map(lambda(v): new_args.append(InteractionComponent(v)), check_args)
        super(InteractionComponentList, self).__init__(new_args)

    def __setitem__(self, ind, value):
        """Provides type checking for setting and item in the list

        :param ind: the index to set
        :type ind: int
        :param value: the value to set at the index
        :type value: :mod:`InteractionComponent`

        """
        if not isinstance(value, InteractionComponent):
            value = InteractionComponent(value)
        super(InteractionComponentList, self).__setitem__(ind, value)

    def append(self, value):
        """Provides error checking when appending to the list

        :param value: the value to append
        :type value: :mod:`InteractionComponent`

        """
        if not isinstance(value, InteractionComponent):
            value = InteractionComponent(value)
        super(InteractionComponentList, self).append(value)

    def extend(self, value):
        """Provides error checking when extending the list

        This method will check every argument in the argument list
        to ensure it is of type :mod:`InteractionComponent` before extending
        the current list

        :param value: The list that self will extend
        :type value: :mod:`InteractionComponentList` | list of InteractionComponents

        """
        new_args = []
        map(lambda(v): new_args.append(InteractionComponent(v)), value)
        super(InteractionComponentList, self).extend(new_args)

    def insert(self, ind, value):
        """Provides error checking when inserting into the list

        :param ind: the index to set
        :type ind: int
        :param value: the value to set at the index
        :type value: :mod:`InteractionComponent`

        """
        if not isinstance(value, InteractionComponent):
            value = InteractionComponent(value)
        super(InteractionComponentList, self).insert(ind, value)

    def _as_version(self, version=Version.latest):
        return list(self)
