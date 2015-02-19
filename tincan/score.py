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


class Score(SerializableBase):
    """Stores the scoring data for an activity.

    Can be created from a dict, another Score, or from kwargs.

    All these attributes are optional and settable to None:

    :param scaled: Scaled score
    :type scaled: float
    :param raw: Raw score
    :type raw: float
    :param min: Minimum score possible
    :type min: float
    :param max: Maximum score possible
    :type max: float
    """

    _props = [
        'scaled',
        'raw',
        'min',
        'max',
    ]

    def __init__(self, *args, **kwargs):
        self._scaled = None
        self._raw = None
        self._min = None
        self._max = None

        super(SerializableBase, self).__init__(*args, **kwargs)

    @property
    def scaled(self):
        """Scaled for Score

        :setter: Tries to convert to float. If None is provided,
        this signifies the absence of this data.
        :setter type: float | int | None
        :rtype: float | None
        :raises: TypeError if unsupported type is provided
        """
        return self._scaled

    @scaled.setter
    def scaled(self, value):
        if value is None or isinstance(value, float):
            self._scaled = value
            return
        try:
            self._scaled = float(value)
        except Exception as e:
            msg = (
                "Property 'scaled' in a 'tincan.%s' object must be set with a "
                "float or None." %
                self.__class__.__name__
            )
            msg += e.message
            raise TypeError(msg)

    @scaled.deleter
    def scaled(self):
        del self._scaled

    @property
    def raw(self):
        """Raw for Score

        :setter: Tries to convert to float. If None is provided,
        this signifies the absence of this data.
        :setter type: float | int | None
        :rtype: float | None
        :raises: TypeError if unsupported type is provided
        """
        return self._raw

    @raw.setter
    def raw(self, value):
        if value is None or isinstance(value, float):
            self._raw = value
            return
        try:
            self._raw = float(value)
        except Exception as e:
            msg = (
                "Property 'raw' in a 'tincan.%s' object must be set with a "
                "float or None." %
                self.__class__.__name__
            )
            msg += e.message
            raise TypeError(msg)

    @raw.deleter
    def raw(self):
        del self._raw

    @property
    def min(self):
        """Min for Score

        :setter: Tries to convert to float. If None is provided,
        this signifies the absence of this data.
        :setter type: float | int | None
        :rtype: float | None
        :raises: TypeError if unsupported type is provided
        """
        return self._min

    @min.setter
    def min(self, value):
        if value is None or isinstance(value, float):
            self._min = value
            return
        try:
            self._min = float(value)
        except Exception as e:
            msg = (
                "Property 'min' in a 'tincan.%s' object must be set with a "
                "float or None." %
                self.__class__.__name__
            )
            msg += e.message
            raise TypeError(msg)

    @min.deleter
    def min(self):
        del self._min

    @property
    def max(self):
        """Max for Score

        :setter: Tries to convert to float. If None is provided,
        this signifies the absence of this data.
        :setter type: float | int | None
        :rtype: float | None
        :raises: TypeError if unsupported type is provided
        """
        return self._max

    @max.setter
    def max(self, value):
        if value is None or isinstance(value, float):
            self._max = value
            return
        try:
            self._max = float(value)
        except Exception as e:
            msg = (
                "Property 'max' in a 'tincan.%s' object must be set with a "
                "float or None." %
                self.__class__.__name__
            )
            msg += e.message
            raise TypeError(msg)

    @max.deleter
    def max(self):
        del self._max
