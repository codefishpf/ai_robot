#!/usr/bin/python3
import math
import time

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range

from controller import mecanum
from ros_robot_controller_msgs.msg import MotorsState

class ObstacleAvoidanceNode(Node):
    def __init__(self):
        super().__init__('obstacle_avoidance')

        self.safe_distance = 0.2  # m
        self.forward_speed = 0.2  # m/s
        self.turn_speed = 0.5     # rad/s

        self.mecanum = mecanum.MecanumChassis()
        self.motor_pub = self.create_publisher(MotorsState, '/ros_robot_controller/set_motor', 1)
        self.ultrasonic_sub = self.create_subscription(Range, '/ros_robot_controller/ultrasonic', self.ultrasonic_callback, 10)

        self.timer = self.create_timer(0.1, self.timer_callback)

        self.state = "FORWARD"
        self.turn_start_time = None
        self.turn_duration = 90.0 / (self.turn_speed * 180.0 / math.pi)

        self.get_logger().info('\033[1;32m%s\033[0m' % 'start')

    def ultrasonic_callback(self, msg):
        self.distance = msg.range
        self.get_logger().info(f'Obstacle distance: {self.distance} m')

        if self.state == "FORWARD" and self.distance < self.safe_distance:
            self.state = "TURNING"
            self.turn_start_time = self.get_clock().now().nanoseconds / 1e9
            self.get_logger().info('Obstacle detected! Start turning.')

    def timer_callback(self):
        now = self.get_clock().now().nanoseconds / 1e9

        if self.state == "FORWARD":
            self.motor_pub.publish(self.mecanum.set_velocity(self.forward_speed, 0.0))

        elif self.state == "TURNING":
            if self.turn_start_time is None:
                self.turn_start_time = now
            elapsed = now - self.turn_start_time

            if elapsed < self.turn_duration:
                self.motor_pub.publish(self.mecanum.set_velocity(0.0, self.turn_speed))
            else:
                self.motor_pub.publish(self.mecanum.set_velocity(0.0, 0.0))
                self.get_logger().info('Turn complete. Resume forward.')
                self.state = "FORWARD"

def main(args=None):
    rclpy.init(args=args)
    node = ObstacleAvoidanceNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
