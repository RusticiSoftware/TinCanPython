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
from tincan.language_map import LanguageMap
from tincan.extensions import Extensions
from tincan.interaction_component_list import InteractionComponentList

"""
.. module:: activitydefinition
   :synopsis: The definition of the Activity object that provides \
   more granular details and extensions

"""


class ActivityDefinition(SerializableBase):
    _props = [
        'name',
        'description',
        'type',
        'more_info',
        'interaction_type',
        'correct_responses_pattern',
        'choices',
        'scale',
        'source',
        'target',
        'steps',
        'extensions',
    ]

    _interaction_types = [
        'choice',
        'sequencing',
        'likert',
        'matching',
        'performance',
        'true-false',
        'fill-in',
        'long-fill-in',
        'numeric',
        'other',
    ]

    def __init__(self, *args, **kwargs):
        self._name = None
        self._description = None
        self._type = None
        self._more_info = None
        self._interaction_type = None
        self._correct_responses_pattern = None
        self._choices = None
        self._scale = None
        self._source = None
        self._target = None
        self._steps = None
        self._extensions = None

        super(ActivityDefinition, self).__init__(*args, **kwargs)

    @property
    def name(self):
        """Name for Activity Definition

        :setter: Tries to convert to :class:`tincan.LanguageMap`
        :setter type: :class:`tincan.LanguageMap`
        :rtype: :class:`tincan.LanguageMap`

        """
        return self._name

    @name.setter
    def name(self, value):
        if value is not None and not isinstance(value, LanguageMap):
            value = LanguageMap(value)
        self._name = value

    @name.deleter
    def name(self):
        del self._name

    @property
    def description(self):
        """Description for Activity Definition

        :setter: Tries to convert to :class:`tincan.LanguageMap`
        :setter type: :class:`tincan.LanguageMap`
        :rtype: :class:`tincan.LanguageMap`

        """
        return self._description

    @description.setter
    def description(self, value):
        if value is not None and not isinstance(value, LanguageMap):
            value = LanguageMap(value)
        self._description = value

    @description.deleter
    def description(self):
        del self._description

    @property
    def type(self):
        """Type for Activity Definition

        :setter: Tries to convert to unicode
        :setter type: unicode
        :rtype: unicode

        """
        return self._type

    @type.setter
    def type(self, value):
        if value is not None:
            if value == '':
                raise ValueError("type cannot be set to an empty string")
            value = str(value)
        self._type = value

    @type.deleter
    def type(self):
        del self._type

    @property
    def more_info(self):
        """More info for Activity Definition

        :setter: Tries to convert to unicode
        :setter type: unicode
        :rtype: unicode

        """
        return self._more_info

    @more_info.setter
    def more_info(self, value):
        if value is not None:
            if value == '':
                raise ValueError("more_info cannot be set to an empty string")
            value = str(value)
        self._more_info = value

    @more_info.deleter
    def more_info(self):
        del self._more_info

    @property
    def interaction_type(self):
        """Interaction type for Activity Definition. Must be a value in interaction_types

        :setter: Tries to convert to unicode
        :setter type: unicode
        :rtype: unicode

        """
        return self._interaction_type

    @interaction_type.setter
    def interaction_type(self, value):
        if value is not None:
            if value not in self._interaction_types:
                raise ValueError("invalid interaction type")
        self._interaction_type = value

    @interaction_type.deleter
    def interaction_type(self):
        del self._interaction_type

    @property
    def correct_responses_pattern(self):
        """Correct responses pattern for Activity Definition

        :setter: Sets the correct responses pattern
        :setter type: list
        :rtype: list

        """
        return self._correct_responses_pattern

    @correct_responses_pattern.setter
    def correct_responses_pattern(self, value):
        if value is not None:
            if not isinstance(value, list):
                raise TypeError("correct responses pattern must be a list")
        self._correct_responses_pattern = value

    @correct_responses_pattern.deleter
    def correct_responses_pattern(self):
        del self._correct_responses_pattern

    @property
    def choices(self):
        """Choices for Activity Definition

        :setter: Tries to convert to :class:`tincan.InteractionComponentList`
        :setter type: :class:`tincan.InteractionComponentList`
        :rtype: :class:`tincan.InteractionComponentList`

        """
        return self._choices

    @choices.setter
    def choices(self, value):
        if value is not None and not isinstance(value, InteractionComponentList):
            value = InteractionComponentList(value)
        self._choices = value

    @choices.deleter
    def choices(self):
        del self._choices

    @property
    def scale(self):
        """Scale for Activity Definition

        :setter: Tries to convert to :class:`tincan.InteractionComponentList`
        :setter type: :class:`tincan.InteractionComponentList`
        :rtype: :class:`tincan.InteractionComponentList`

        """
        return self._scale

    @scale.setter
    def scale(self, value):
        if value is not None and not isinstance(value, InteractionComponentList):
            value = InteractionComponentList(value)
        self._scale = value

    @scale.deleter
    def scale(self):
        del self._scale

    @property
    def source(self):
        """Source for Activity Definition

        :setter: Tries to convert to :class:`tincan.InteractionComponentList`
        :setter type: :class:`tincan.InteractionComponentList`
        :rtype: :class:`tincan.InteractionComponentList`

        """
        return self._source

    @source.setter
    def source(self, value):
        if value is not None and not isinstance(value, InteractionComponentList):
            value = InteractionComponentList(value)
        self._source = value

    @source.deleter
    def source(self):
        del self._source

    @property
    def target(self):
        """Target for Activity Definition

        :setter: Tries to convert to :class:`tincan.InteractionComponentList`
        :setter type: :class:`tincan.InteractionComponentList`
        :rtype: :class:`tincan.InteractionComponentList`

        """
        return self._target

    @target.setter
    def target(self, value):
        if value is not None and not isinstance(value, InteractionComponentList):
            value = InteractionComponentList(value)
        self._target = value

    @target.deleter
    def target(self):
        del self._target

    @property
    def steps(self):
        """Steps for Activity Definition

        :setter: Tries to convert to :class:`tincan.InteractionComponentList`
        :setter type: :class:`tincan.InteractionComponentList`
        :rtype: :class:`tincan.InteractionComponentList`

        """
        return self._steps

    @steps.setter
    def steps(self, value):
        if value is not None and not isinstance(value, InteractionComponentList):
            value = InteractionComponentList(value)
        self._steps = value

    @steps.deleter
    def steps(self):
        del self._steps

    @property
    def extensions(self):
        """Extensions for Activity Definition

        :setter: Tries to convert to :class:`tincan.Extensions`
        :setter type: :class:`tincan.Extensions`
        :rtype: :class:`tincan.Extensions`

        """
        return self._extensions

    @extensions.setter
    def extensions(self, value):
        if value is not None and not isinstance(value, Extensions):
            value = Extensions(value)
        self._extensions = value

    @extensions.deleter
    def extensions(self):
        del self._extensions
