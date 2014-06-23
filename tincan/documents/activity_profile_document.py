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
from tincan.documents import Document
from tincan.activity import Activity


class ActivityProfileDocument(Document):
    """Extends Document with an Activity field, can be created from a dict, another Document, or from kwargs.

    :param id: The id of this document
    :type id: unicode
    :param content_type: The content_type of the content of this document
    :type content_type: unicode
    :param content: The content of this document
    :type content: bytearray
    :param etag: The etag of this document
    :type etag: unicode
    :param timestamp: The timestamp of this document
    :type timestamp: :mod:`datetime.datetime`
    :param activity: The activity object of this document
    :type activity: Activity
    """

    _props_req = list(Document._props_req)

    _props_req.extend([
        'activity',
    ])

    _props = list(Document._props)

    _props.extend(_props_req)

    @property
    def activity(self):
        """The Document's activity object

        :setter: Tries to convert to activity
        :setter type: :class:`tincan.activity.Activity`
        :rtype: :class:`tincan.activity.Activity`
        """
        return self._activity

    @activity.setter
    def activity(self, value):
        if not isinstance(value, Activity) and value is not None:
            try:
                value = Activity(value)
            except:
                raise TypeError(
                    "Property 'activity' in 'tincan.documents.%s' must be set with a type "
                    "that can be constructed into an Activity object." % self.__class__.__name__
                )
        self._activity = value
