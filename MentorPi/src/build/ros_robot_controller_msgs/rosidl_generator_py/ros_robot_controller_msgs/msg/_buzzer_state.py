# generated from rosidl_generator_py/resource/_idl.py.em
# with input from ros_robot_controller_msgs:msg/BuzzerState.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_BuzzerState(type):
    """Metaclass of message 'BuzzerState'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('ros_robot_controller_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'ros_robot_controller_msgs.msg.BuzzerState')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__buzzer_state
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__buzzer_state
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__buzzer_state
            cls._TYPE_SUPPORT = module.type_support_msg__msg__buzzer_state
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__buzzer_state

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class BuzzerState(metaclass=Metaclass_BuzzerState):
    """Message class 'BuzzerState'."""

    __slots__ = [
        '_freq',
        '_on_time',
        '_off_time',
        '_repeat',
    ]

    _fields_and_field_types = {
        'freq': 'uint16',
        'on_time': 'float',
        'off_time': 'float',
        'repeat': 'uint16',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('uint16'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint16'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.freq = kwargs.get('freq', int())
        self.on_time = kwargs.get('on_time', float())
        self.off_time = kwargs.get('off_time', float())
        self.repeat = kwargs.get('repeat', int())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.freq != other.freq:
            return False
        if self.on_time != other.on_time:
            return False
        if self.off_time != other.off_time:
            return False
        if self.repeat != other.repeat:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def freq(self):
        """Message field 'freq'."""
        return self._freq

    @freq.setter
    def freq(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'freq' field must be of type 'int'"
            assert value >= 0 and value < 65536, \
                "The 'freq' field must be an unsigned integer in [0, 65535]"
        self._freq = value

    @builtins.property
    def on_time(self):
        """Message field 'on_time'."""
        return self._on_time

    @on_time.setter
    def on_time(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'on_time' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'on_time' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._on_time = value

    @builtins.property
    def off_time(self):
        """Message field 'off_time'."""
        return self._off_time

    @off_time.setter
    def off_time(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'off_time' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'off_time' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._off_time = value

    @builtins.property
    def repeat(self):
        """Message field 'repeat'."""
        return self._repeat

    @repeat.setter
    def repeat(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'repeat' field must be of type 'int'"
            assert value >= 0 and value < 65536, \
                "The 'repeat' field must be an unsigned integer in [0, 65535]"
        self._repeat = value
