from launch import LaunchDescription
import launch_ros.actions
import logging
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    print('ascamera launch node with depthimage to laserscan')
    return LaunchDescription([
        launch_ros.actions.Node(
            namespace="ascamera",
            package='ascamera',
            executable='ascamera_node',
            respawn=True,
            output='both',
            parameters=[
                {"usb_bus_no": -1},
                {"usb_path": "null"},
                {"confiPath": "/home/ubuntu/third_party_ros2/third_party_ws/src/ascamera/configurationfiles"},
                {"color_pcl": True},
                {"pub_tfTree": True},
                {"depth_width": 640},
                {"depth_height": 480},
                {"rgb_width": 640},
                {"rgb_height": 480},
                {"fps": 15},
            ]

        ),
        Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        #arguments = ['0', '0', '0', '-1.57', '0', '-1.57', 'depth_cam', 'ascamera_camera_link_0']
        arguments = ['0', '0', '0', '-1.57', '0', '-1.57', 'depth_cam', 'ascamera_camera_link_0']
        ),
        
        
        Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        #arguments = ['0', '0', '0', '-1.57', '0', '-1.57', 'depth_cam', 'ascamera_camera_link_0']
        arguments = ['0', '0', '0', '-1.57', '0', '-1.57', 'depth_cam', 'ascamera_color_0']
        ),
        
        # depth to scan
        # 深度图转激光扫描
        # Node(
        #     package='depthimage_to_laserscan',
        #     executable='depthimage_to_laserscan_node',
        #     name='depthimage_to_laserscan',
        #     parameters=[{
        #         'output_frame': 'camera_link',
        #         'scan_height': 1,          # 单线扫描
        #         'range_min': 0.3,          # 最小距离0.3米
        #         'range_max': 8.0,          # 最大距离8米
        #         'scan_time': 0.033,        # 30Hz更新
        #     }],
        #     remappings=[
        #         # ('depth', '/camera/depth/image_rect_raw'),
        #         # ('depth_camera_info', '/camera/depth/camera_info')
        #         # ('rgb/camera_info', '/ascamera/camera_publisher/rgb0/camera_info'),
        #         # ('depth/image', '/ascamera/camera_publisher/depth0/image_raw'),
        #         ('/ascamera/camera_publisher/depth0/image_raw', '/camera/depth/image_rect_raw'),
        #         ('/ascamera/camera_publisher/rgb0/camera_info', '/camera/depth/camera_info'),
        #         ('scan', '/scan')        # 输出话题名
        #     ]
        # ),

        # 坐标系对齐（base_link -> camera_link）
        # Node(
        #     package='tf2_ros',
        #     executable='static_transform_publisher',
        #     arguments=['0.1', '0', '0.2', '0', '0', '0', 'base_link', 'camera_link']
        # )
      
      ])

if __name__ == '__main__':
    # 创建一个LaunchDescription对象(create a LaunchDescription object)
    ld = generate_launch_description()

    ls = LaunchService()
    ls.include_launch_description(ld)
    ls.run()