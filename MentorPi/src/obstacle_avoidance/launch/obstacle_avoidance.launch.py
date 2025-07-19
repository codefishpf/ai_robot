from launch_ros.actions import Node
from launch import LaunchDescription, LaunchService
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    imu_frame = LaunchConfiguration('imu_frame', default='imu_link')
    imu_frame_arg = DeclareLaunchArgument('imu_frame', default_value=imu_frame)

    ros_robot_controller_node = Node(
        package='ros_robot_controller',
        executable='ros_robot_controller',
        output='screen',
        parameters=[{'imu_frame': imu_frame}]
    )

    obstacle_avoidance_node = Node(
        package='obstacle_avoidance',
        executable='obstacle_avoidance',
        output='screen',
    )

    return LaunchDescription([
        imu_frame_arg,
        ros_robot_controller_node,
        obstacle_avoidance_node,
    ])
