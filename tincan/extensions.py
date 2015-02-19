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


class Extensions(dict, SerializableBase):
    """
    Contains domain-specific custom data.

    Can be created from a dict, another :class:`tincan.Extensions`,
    or from args and kwargs.

    Use this like a regular Python dict.
    """

    def __init__(self, *args, **kwargs):
        super(Extensions, self).__init__(*args, **kwargs)
