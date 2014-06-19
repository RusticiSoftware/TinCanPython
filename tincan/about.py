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
from tincan.version import Version
from tincan.extensions import Extensions


class About(SerializableBase):
    _props_req = [
        'version',
    ]
    _props = [
        'extensions',
    ]
    _props.extend(_props_req)


    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        """Setter for the _version attribute. Makes sure that the
        versions given are supported before setting.

        :param value: list of the versions supported
        :type value: list | tuple | None
        """
        def check_version(v):
            """Checks a single version string for validity. Raises
            if invalid.

            :param v: the version string to check
            :raises ValueError
            """
            if v in Version.supported:
                return

            # Construct the error message
            if isinstance(value, (list, tuple)):
                value_str = repr(v) + ' in ' + repr(value)
            else:
                value_str = repr(v)

            msg = (
                "Tried to set property 'version' in a 'tincan.%s' object "
                "with an invalid value: %s\n"
                "Allowed versions are: %s" %
                (
                    self.__class__.__name__,
                    value_str,
                    ', '.join(map(repr, Version.supported)),
                )
            )

            raise ValueError(msg)


        if value is None:
            self._version = [Version.latest]
        elif isinstance(value, basestring):
            check_version(value)
            self._version = [value]
        elif isinstance(value, (list, tuple)):
            for v in value:
                check_version(v)
            self._version = list(value)
        else:
            raise TypeError(
                "Property 'version' in a 'tincan.%s' object must be set with a "
                "list, tuple, str, unicode or None. Tried to set it with: %s" %
                (
                    self.__class__.__name__,
                    repr(value),
                ))


    @property
    def extensions(self):
        return self._extensions

    @extensions.setter
    def extensions(self, value):
        """Setter for the _extensions attribute. Tries to convert to Extensions.

        :param value: the Extensions for this installation of TinCan.
        """

        if isinstance(value, Extensions):
            self._extensions = value
        elif value is None:
            self._extensions = Extensions()
        else:
            try:
                self._extensions = Extensions(value)
            except Exception as e:
                msg = (
                    "Property 'extensions' in a 'tincan.%s' object must be set with an "
                    "Extensions, dict, or None.\n\n" %
                    self.__class__.__name__,
                )
                msg += e.message
                raise TypeError(msg)

    @extensions.deleter
    def extensions(self):
        del self._extensions