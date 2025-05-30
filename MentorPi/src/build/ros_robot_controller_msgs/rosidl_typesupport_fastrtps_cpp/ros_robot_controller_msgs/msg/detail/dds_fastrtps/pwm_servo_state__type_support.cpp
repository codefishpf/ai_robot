// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from ros_robot_controller_msgs:msg/PWMServoState.idl
// generated code does not contain a copyright notice
#include "ros_robot_controller_msgs/msg/detail/pwm_servo_state__rosidl_typesupport_fastrtps_cpp.hpp"
#include "ros_robot_controller_msgs/msg/detail/pwm_servo_state__struct.hpp"

#include <limits>
#include <stdexcept>
#include <string>
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_fastrtps_cpp/wstring_conversion.hpp"
#include "fastcdr/Cdr.h"


// forward declaration of message dependencies and their conversion functions

namespace ros_robot_controller_msgs
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_ros_robot_controller_msgs
cdr_serialize(
  const ros_robot_controller_msgs::msg::PWMServoState & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: id
  {
    cdr << ros_message.id;
  }
  // Member: position
  {
    cdr << ros_message.position;
  }
  // Member: offset
  {
    cdr << ros_message.offset;
  }
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_ros_robot_controller_msgs
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  ros_robot_controller_msgs::msg::PWMServoState & ros_message)
{
  // Member: id
  {
    cdr >> ros_message.id;
  }

  // Member: position
  {
    cdr >> ros_message.position;
  }

  // Member: offset
  {
    cdr >> ros_message.offset;
  }

  return true;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_ros_robot_controller_msgs
get_serialized_size(
  const ros_robot_controller_msgs::msg::PWMServoState & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: id
  {
    size_t array_size = ros_message.id.size();

    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    size_t item_size = sizeof(ros_message.id[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: position
  {
    size_t array_size = ros_message.position.size();

    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    size_t item_size = sizeof(ros_message.position[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: offset
  {
    size_t array_size = ros_message.offset.size();

    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    size_t item_size = sizeof(ros_message.offset[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_ros_robot_controller_msgs
max_serialized_size_PWMServoState(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;


  // Member: id
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);

    last_member_size = array_size * sizeof(uint16_t);
    current_alignment += array_size * sizeof(uint16_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint16_t));
  }

  // Member: position
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);

    last_member_size = array_size * sizeof(uint16_t);
    current_alignment += array_size * sizeof(uint16_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint16_t));
  }

  // Member: offset
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);

    last_member_size = array_size * sizeof(uint16_t);
    current_alignment += array_size * sizeof(uint16_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint16_t));
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = ros_robot_controller_msgs::msg::PWMServoState;
    is_plain =
      (
      offsetof(DataType, offset) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static bool _PWMServoState__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const ros_robot_controller_msgs::msg::PWMServoState *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _PWMServoState__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<ros_robot_controller_msgs::msg::PWMServoState *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _PWMServoState__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const ros_robot_controller_msgs::msg::PWMServoState *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _PWMServoState__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_PWMServoState(full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}

static message_type_support_callbacks_t _PWMServoState__callbacks = {
  "ros_robot_controller_msgs::msg",
  "PWMServoState",
  _PWMServoState__cdr_serialize,
  _PWMServoState__cdr_deserialize,
  _PWMServoState__get_serialized_size,
  _PWMServoState__max_serialized_size
};

static rosidl_message_type_support_t _PWMServoState__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_PWMServoState__callbacks,
  get_message_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace ros_robot_controller_msgs

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_ros_robot_controller_msgs
const rosidl_message_type_support_t *
get_message_type_support_handle<ros_robot_controller_msgs::msg::PWMServoState>()
{
  return &ros_robot_controller_msgs::msg::typesupport_fastrtps_cpp::_PWMServoState__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, ros_robot_controller_msgs, msg, PWMServoState)() {
  return &ros_robot_controller_msgs::msg::typesupport_fastrtps_cpp::_PWMServoState__handle;
}

#ifdef __cplusplus
}
#endif
