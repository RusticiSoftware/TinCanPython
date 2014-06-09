"""
    Copyright 2014 Rustici Software

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

from tincanbase import TinCanBaseObject
from languagemap import LanguageMap

"""
.. module:: verb
   :synopsis: A Verb object that contains an id and a display

"""


class Verb(TinCanBaseObject):

    def __init__(self, id=None, display=None):
        """Initializes a Verb Object with the given id and display

        :param verb_id: The id of the verb
        :type verb_id: str
        :param display: The LanguageMap indicating how the verb object \
        should be displayed
        :type display: dict, :mod:`LanguageMap`

        """
        self.set_id(id)
        self.set_display(display)

    def __repr__(self):
        return 'Verb: %s' % self.__dict__

    def set_id(self, id):
        """Provides error checking when setting the id property

        :param id: The desired value for id
        :type id: str

        :raises: ValueError

        """
        if id is not None:
            if id == '' or not isinstance(id, basestring):
                raise ValueError("id cannot be set to an empty string or non-string type")
        self.id = id

    def get_id(self):
        """Retrieve the id of the verb
        """
        return self.id

    def set_display(self, display):
        """Provides error checking when setting the display property

        :param display: The desired value for display
        :type display: dict, :mod:`LanguageMap`

        """
        if display is not None:
            if not display:
                display = None
            elif not isinstance(display, LanguageMap):
                display = LanguageMap(display)
            elif len(vars(display)) == 0:
                display = None
        self.display = display

    def get_display(self):
        """Retrieve the display of the verb
        """
        return self.display

