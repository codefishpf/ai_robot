#!/usr/bin/env python3
# encoding: utf-8

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu

class IMUSubscriber(Node):
    def __init__(self):
        super().__init__('imu_subscriber')
        
        self.declare_parameter('imu_topic', '/ros_robot_controller/imu_raw')
        self.imu_topic = self.get_parameter('imu_topic').get_parameter_value().string_value

        self.subscription = self.create_subscription(
            Imu,
            self.imu_topic,
            self.listener_callback,
            10)
        
        self.subscription  # prevent unused variable warning
        self.get_logger().info(f'Subscribed to {self.imu_topic}')

    def listener_callback(self, msg):
        orientation = msg.orientation
        angular_velocity = msg.angular_velocity
        linear_acceleration = msg.linear_acceleration

        self.get_logger().info(f'Orientation: x={orientation.x}, y={orientation.y}, z={orientation.z}, w={orientation.w}')
        self.get_logger().info(f'Angular Velocity: x={angular_velocity.x}, y={angular_velocity.y}, z={angular_velocity.z}')
        self.get_logger().info(f'Linear Acceleration: x={linear_acceleration.x}, y={linear_acceleration.y}, z={linear_acceleration.z}')

def main(args=None):
    rclpy.init(args=args)
    node = IMUSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

