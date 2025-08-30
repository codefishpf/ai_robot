import os
from launch import LaunchDescription, LaunchService
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

# Just for test ultrasonic.
# (1) Launch this launch file.
# (2) Run: ros2 action send_goal /navigate_to_pose nav2_msgs/action/NavigateToPose "
# pose: {
#   header: {frame_id: 'odom'},
#   pose: {
#     position: {x: 1.0, y: 0.0, z: 0.0},
#     orientation: {z: 0.0, w: 1.0}
#   }
# }"
# (3) But the car can not move, due to planer and global cost map.
def generate_launch_description():
    # 获取编译环境变量
    compiled = os.environ.get('need_compile', 'False')  # 使用get方法避免键不存在时报错
    
    if compiled == 'True':
        robot_controller_package_path = get_package_share_directory('ros_robot_controller')
        navigation_package_path = get_package_share_directory('navigation')
    else:
        robot_controller_package_path = '/home/ubuntu/ros2_ws/src/driver/ros_robot_controller'
        navigation_package_path = '/home/ubuntu/ros2_ws/src/navigation'
    
    # 参数文件路径
    params_file = os.path.join(
        navigation_package_path, 'config/nav2_params_single_ultrasonic_test.yaml')
    
    # 定义生命周期节点列表
    lifecycle_nodes = ['controller_server', 'planner_server', 'behavior_server', 'bt_navigator']
    
    return LaunchDescription([
        # Navigation2 控制器
        Node(
            package='nav2_controller',
            executable='controller_server',
            name='controller_server',
            parameters=[params_file],
            output='screen'
        ),
        
        # 规划器服务器（必须添加以实现目标点导航）
        Node(
            package='nav2_planner',
            executable='planner_server',
            name='planner_server',
            parameters=[params_file],
            output='screen'
        ),
        
        # 行为服务器（处理恢复行为）
        Node(
            package='nav2_behaviors',
            executable='behavior_server',
            name='behavior_server',
            parameters=[params_file],
            output='screen'
        ),
        
        # BT导航器（处理导航目标）
        Node(
            package='nav2_bt_navigator',
            executable='bt_navigator',
            name='bt_navigator',
            parameters=[params_file],
            output='screen'
        ),
        
        # 生命周期管理器（管理所有Navigation2节点）
        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager',
            output='screen',
            parameters=[{
                'autostart': True,
                'node_names': lifecycle_nodes  # 管理所有Navigation2节点
            }]
        ),
        
        # 静态TF广播（确保超声波坐标系存在）
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=['0.2', '0', '0.1', '0', '0', '0', 'base_link', 'ultrasonic_link'],
            name='ultrasonic_tf_publisher'
        ),

        # 静态TF广播（确保imu坐标系存在）
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=['0.0', '0', '0.0', '0', '0', '0', 'base_link', 'imu_link'],
            name='imu_tf_publisher'
        ),

        # 发布 odom 到 base_link 的静态变换（如果没有里程计）
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=['0', '0', '0', '0', '0', '0', 'odom', 'base_link'],
            name='odom_to_base_link_tf'
        ),

        # 超声波驱动节点
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                os.path.join(robot_controller_package_path, 'launch/ros_robot_controller.launch.py')
            ])
        )
    ])

if __name__ == '__main__':
    # 创建一个LaunchDescription对象
    ld = generate_launch_description()

    ls = LaunchService()
    ls.include_launch_description(ld)
    ls.run()