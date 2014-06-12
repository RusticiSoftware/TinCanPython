#!/usr/bin/env python

from tincan.tincanbase import TinCanBaseObject
from tincan.score import Score
from tincan.extensions import Extensions
from tincan.version import Version
##TODO: add converters for ISO 8601 duration <-> timedelta
# from tincan.iso8601 import make_timedelta, make_duration

from datetime import timedelta
from inspect import isclass


def make_bytearray(value):
    if isinstance(value, unicode):
        return bytearray(value, 'utf-8')
    else:
        return bytearray(value)


def jsonify_bytearray(value):
    return value.decode('utf-8')

class Result(TinCanBaseObject):
    """
    Stores the state of an activity.
    """
    ## _props_in_conversions__<version>:
    # A dict that specifies how to auto convert stuff to
    # Python-friendly types. This is used during construction and
    # when setting properties to make sure the types are what we
    # expect, and to convert them if not.
    #
    # Example:
    # {
    #   'prop1': MyClass,
    #   'prop2': {'type': MyClass},     # same behavior as prop1
    #   'prop3': {'type': MyClass, 'converter': make_myclass},
    # }
    _props_in_conversions = {
        'score': Score,
        'success': bool,
        'completion': bool,
        ##TODO: add converters for ISO 8601 duration <-> timedelta
        # 'duration': {'type': timedelta, 'converter': make_timedelta,},
        'duration': str,
        'response': {'type': bytearray, 'converter': make_bytearray},
        'extensions': Extensions,
    }

    ## _props_out_conversions__<version>:
    # A dict that specifies how objects should be converted to JSON-
    # friendly forms. This is only used if the property is
    # not a subclass of TinCanBaseObject.
    #
    # Example:
    # {
    #   'prop1': myclass_to_json,   # not needed if MyClass extends
    # }                             # TinCanBaseObject or is already
    #                               # JSON-friendly.
    _props_out_conversions__default = {
        ##TODO: add converters for ISO 8601 duration <-> timedelta
        # 'duration': make_duration,
        'response': jsonify_bytearray,
    }

    ## _props_format_versions:
    # A dict that specifies which properties are present and how they
    # should be formatted for different versions of TinCan. If the
    # version sought is not explicitly present here, the 'default'
    # schema will be used. Each schema is a dict of 'in'-conversions
    # to Python-friendly types and 'out'-conversions to JSON-friendly
    # types. See above for info on these dicts.
    _props_out_conversions_versions = {
        'default': _props_out_conversions__default,
        # '1.0.0': _props_out_conversions__1_0_x
        # '1.0.1': _props_out_conversions__1_0_x
    }

    def _props_out_conversions(self, version=Version.latest):
        return self._props_out_conversions_versions.get(version) or \
               self._props_out_conversions_versions['default']

    @property
    def _props_allowed(self):
        return self._props_in_conversions.keys()

    def __init__(self, *args, **kwargs):
        """
        :param score: Contains the score and its scaling information
        :type score: Score
        :param success: Whether successful
        :type success: bool
        :param completion: Whether completed
        :type completion: bool
        :param duration: How long it took
        :type duration: timedelta
        :param response: HTTPResponse data
        :type response: bytearray
        :param extensions: Custom user data
        :type extensions: Extensions
        """
        self._version = kwargs.pop('version', Version.latest)

        # Copy construction
        if args and len(args) == 1:
            obj = args[0]

            # Copy properties from obj
            new_kwargs = obj if isinstance(obj, dict) else obj.__dict__

            # make kwargs overwrite fields of copied object
            if kwargs:
                new_kwargs.update(kwargs)
            kwargs = new_kwargs

        # Only use the properties in self._allowed_properties
        filtered_keys = [k for k in kwargs if k in self._props_allowed]
        for k in filtered_keys:
            setattr(self, k, kwargs[k])

    def __setattr__(self, attr, value):
        """
        Converts to TinCan objects if possible.
        """
        if attr == '_version':
            self.__dict__[attr] = value
        elif attr not in self._props_allowed:
            raise AttributeError(
                "Attribute '%s' of '%s' object cannot be set. Allowed attributes: %s" %
                (
                    attr,
                    self.__class__.__name__,
                    ', '.join(self._props_allowed)
                ))
        elif value is not None and attr in self._props_in_conversions:
            conversion = self._props_in_conversions[attr]

            if isclass(conversion):
                prop_type = conversion
                prop_converter = conversion
            else:
                prop_type = conversion['type']
                prop_converter = conversion.get('converter', prop_type)

            try:
                self.__dict__[attr] = value if isinstance(value, prop_type) else prop_converter(value)
            except Exception as e:
                raise ValueError('The in-converter for tincan.%s.%s (type: %s) could not process the %s object: %s' % (
                    self.__class__.__name__,
                    attr,
                    prop_type.__name__,
                    value.__class__.__name__,
                    repr(value)
                ))
        else:
            self.__dict__[attr] = value

    def _as_version(self, version=Version.latest):
        """
        Creates a ``dict`` version of self ready for ``to_json()``.

        :param version: A version specifier, eg. "1.0.1"
        :type version: str
        :return: A new ``dict`` object ready for ``to_json()`` to
        serialize.
        """
        # Doesn't work, since underscore variables end up making errors on serializing:
        # result = dict(self.__dict__)
        result = {k: v for k, v in vars(self).iteritems() if not k.startswith('_')}

        # Perform the out-conversion on attributes that need it
        for attr, value in result.iteritems():
            if value is None:
                del result[attr]
            elif isinstance(value, TinCanBaseObject):
                result[attr] = value.as_version(version)
            elif attr in self._props_out_conversions(version):
                converter = self._props_out_conversions(version)[attr]
                assert callable(converter), "The out-converter for version %s in tincan.%s.%s is not a callable" % (
                    version,
                    self.__class__.__name__,
                    attr,
                )

                result[attr] = converter(value)

        return result

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__
