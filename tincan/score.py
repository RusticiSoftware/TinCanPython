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


class Score(SerializableBase):

    """Contains the scaled, raw, min and max scores.

    Can be created from either a dict, another Score, or from kwargs.

    :param scaled: scaled score, 0.0-1.0
    :type scaled: float
    :param raw: raw score
    :type raw: float
    :param min: minimum score possible
    :type min: float
    :param max: maximum score possible
    :type max: float
    """

    _props = [
        'scaled',
        'raw',
        'min',
        'max',
    ]

    @property
    def scaled(self):
        return self._scaled

    @scaled.setter
    def scaled(self, value):
        """Setter for the _scaled attribute. Tries to convert to float.

        :param value: the scaled score, 0.0-1.0
        :type value: float | None
        """

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
        return self._raw

    @raw.setter
    def raw(self, value):
        """Setter for the _raw attribute. Tries to convert to float.

        :param value: the raw score
        :type value: float | None
        """
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
        return self._min

    @min.setter
    def min(self, value):
        """Setter for the _min attribute. Tries to convert to float.

        :param value: the minimum possible score
        :type value: float | None
        """

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
        return self._max

    @max.setter
    def max(self, value):
        """Setter for the _max attribute. Tries to convert to float.

        :param value: the maximum possible score
        :type value: float | None
        """

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

