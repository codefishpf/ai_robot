set(_AMENT_PACKAGE_NAME "interfaces")
set(interfaces_VERSION "0.0.0")
set(interfaces_MAINTAINER "ubuntu <1270161395@qq.com>")
set(interfaces_BUILD_DEPENDS "rosidl_default_generators" "builtin_interfaces" "std_msgs" "geometry_msgs")
set(interfaces_BUILDTOOL_DEPENDS "ament_cmake")
set(interfaces_BUILD_EXPORT_DEPENDS "builtin_interfaces" "std_msgs" "geometry_msgs")
set(interfaces_BUILDTOOL_EXPORT_DEPENDS )
set(interfaces_EXEC_DEPENDS "rosidl_default_runtime" "builtin_interfaces" "std_msgs" "geometry_msgs")
set(interfaces_TEST_DEPENDS "ament_lint_auto" "ament_lint_common")
set(interfaces_GROUP_DEPENDS )
set(interfaces_MEMBER_OF_GROUPS "rosidl_interface_packages")
set(interfaces_DEPRECATED "")
set(interfaces_EXPORT_TAGS)
list(APPEND interfaces_EXPORT_TAGS "<build_type>ament_cmake</build_type>")
list(APPEND interfaces_EXPORT_TAGS "<ros1_bridge mapping_rules=\"mapping_rules.yaml\"/>")
