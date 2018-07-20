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

"""
.. module:: base
   :synopsis: A base object to provide a common initializer for objects to
   easily keep track of required and optional properties and their
   error checking

"""


class Base(object):
    _props = []

    def __init__(self, *args, **kwargs):
        """Initializes an object by checking the provided arguments
        against lists defined in the individual class. If required
        properties are defined, this method will set them to None by default.
        Optional properties will be ignored if they are not provided. The
        class may provide custom setters for properties, in which case those
        setters (see __setattr__ below).

        """
        if hasattr(self, '_props_req') and self._props_req:
            list(map(lambda k: setattr(self, k, None), self._props_req))

        new_kwargs = {}
        for obj in args:
            new_kwargs.update(obj if isinstance(obj, dict) else vars(obj))

        new_kwargs.update(kwargs)

        for key, value in new_kwargs.items():
            setattr(self, key, value)

    def __setattr__(self, attr, value):
        """Makes sure that only allowed properties are set. This method will
        call the proper attribute setter as defined in the class to provide
        additional error checking

        :param attr: the attribute being set
        :type attr: str
        :param value: the value to set

        """
        if attr.startswith('_') and attr[1:] in self._props:
            super(Base, self).__setattr__(attr, value)
        elif attr not in self._props:
            raise AttributeError(
                "Property '%s' cannot be set on a 'tincan.%s' object. Allowed properties: %s" %
                (
                    attr,
                    self.__class__.__name__,
                    ', '.join(self._props)
                ))
        else:
            super(Base, self).__setattr__(attr, value)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__
