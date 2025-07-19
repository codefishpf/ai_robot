#!/usr/bin/env python3
# encoding: utf-8

import rclpy
from rclpy.node import Node
from std_msgs.msg import UInt16

class UltrasonicSubscriber(Node):
    def __init__(self):
        super().__init__('ultrasonic_subscriber')
        
        self.declare_parameter('ultrasonic_topic', '/ros_robot_controller/ultrasonic')
        self.ultrasonic_topic = self.get_parameter('ultrasonic_topic').get_parameter_value().string_value

        self.subscription = self.create_subscription(
            UInt16,
            self.ultrasonic_topic,
            self.listener_callback,
            10)
        
        self.subscription  # prevent unused variable warning
        self.get_logger().info(f'Subscribed to {self.ultrasonic_topic}')

    def listener_callback(self, msg):
        self.get_logger().info(f'Obstacle distance: {msg.data} mm')

def main(args=None):
    rclpy.init(args=args)
    node = UltrasonicSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

