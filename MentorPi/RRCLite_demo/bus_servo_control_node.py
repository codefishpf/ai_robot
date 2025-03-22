#!/usr/bin/env python3
# encoding: utf-8

import rclpy
from rclpy.node import Node
from ros_robot_controller_msgs.msg import ServosPosition, ServoPosition

class BusServoControlNode(Node):
    def __init__(self):
        super().__init__('bus_servo_control_node')
        self.publisher = self.create_publisher(ServosPosition, '/ros_robot_controller/bus_servo/set_position', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.position = 500
        self.moving_up = True

    def timer_callback(self):
        msg = ServosPosition()
        msg.duration = 0.5
        servo_position = ServoPosition()
        servo_position.id = 1
        servo_position.position = self.position
        msg.position = [servo_position]

        self.publisher.publish(msg)
        self.get_logger().info(f'Sent command to move servo 1 to position {self.position}')

        # Alternate position for demonstration
        if self.moving_up:
            self.position += 200
            if self.position >= 1000:
                self.moving_up = False
        else:
            self.position -= 200
            if self.position <= 0:
                self.moving_up = True

def main(args=None):
    rclpy.init(args=args)
    node = BusServoControlNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

