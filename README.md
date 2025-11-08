# ai_robot
We are going to make a fantastic ai robot
## Project description
https://docs.qq.com/doc/DQ29SRmpmSHdkWlp1

## Project documents
https://docs.qq.com/desktop/mydoc/folder/CdleawzNdyET


## Launch Framework
### Navigation mode 
**rtabmap_navigation.launch.py** （开启导航launch文件）
- **base_launch** (slam/launch/include/robot.launch.py) （启动机器人硬件/相关外设）
    - **depth_camera_launch** (peripherals/launch/depth_camera.launch.py)
        - **camera_launch** (peripherals/launch/include/ascamera.launch.py)
        - Node: **ascamera_node** （深度相机）
        - Node: **static_transform_publisher** （发布相机tf）
    - **controller_launch** (driver/controller/launch/controller.launch.py)
        - **imu_filter_launch** (peripherals/launch/imu_filter.launch.py)
            - Node: **imu_filter_node**
            - Node: **imu_calib_node**
        - **odom_publisher_launch** (MentorPi/src/driver/controller/launch/odom_publisher.launch.py)
            - **robot_description_launch** (MentorPi/src/simulations/mentorpi_description/launch/robot_description.launch.py) （机器人URDF）
                - **joint_state_publisher_node**
                - **robot_state_publisher_node**
                - **joint_state_publisher_gui_node**
                - **rviz_launch** (MentorPi/src/simulations/mentorpi_description/launch/rviz.launch.py)
                    - Node: **rviz2**
            - **robot_controller_launch** (MentorPi/src/driver/ros_robot_controller/launch/ros_robot_controller.launch.py)
                - **ros_robot_controller_node** （机器人底盘控制，扩展板通讯）
            - **odom_publisher_node** 
        - **ekf_filter_node** （机器人定位，imu与odom融合，实时位姿，动态tf发布）
    - **joystick_control_launch** (MentorPi/src/peripherals/launch/joystick_control.launch.py)
        - **joy_node** （app控车？）
        - **joystick_control_node** （手柄控车）
- **navigation_launch** (navigation/launch/include/bringup.launch.py)
    - Node: **nav2_container**
    - **localization.launch.py** (navigation/launch/include/localization.launch.py)
        - ComposableNode: **map_server** (nav2_map_server::MapServer)
        - ComposableNode: **amcl** (nav2_amcl::AmclNode)
        - ComposableNode: **lifecycle_manager_localization** (nav2_lifecycle_manager::LifecycleManager)
    - **navigation_base.launch.py**
        - ComposableNode: **controller_server** (nav2_controller::ControllerServer)
        - ComposableNode: **smoother_server** (nav2_smoother::SmootherServer)
        - ComposableNode: **planner_server** (nav2_planner::PlannerServer)
        - ComposableNode: **behavior_server** (behavior_server::BehaviorServer)
        - ComposableNode: **bt_navigator** (nav2_bt_navigator::BtNavigator)
        - ComposableNode: **waypoint_follower** (nav2_waypoint_follower::WaypointFollower)
        - ComposableNode: **velocity_smoother** (nav2_velocity_smoother::VelocitySmoother)
        - ComposableNode: **lifecycle_manager_navigation** (nav2_lifecycle_manager::LifecycleManager)
- **depthimage_to_laserscan_launch**
    - **launch/depthimage_to_laserscan-launch.py** (depthimage_to_laserscan/launch/depthimage_to_laserscan-launch.py)
        - Node: **depthimage_to_laserscan** （深度图转LaserScan）
- **rtabmap_launch** (navigation/launch/include/rtabmap.launch.py)
    - Node: **rtabmap_sync** (::rgbd_sync)
    - Node: **rtabmap_slam** (::rtabmap)
