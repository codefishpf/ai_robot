#!/usr/bin/env python3
# encoding: utf-8
# Date:2021/08/12

import rclpy
from rclpy.node import Node
import signal
from ros_robot_controller_msgs.msg import SetBusServoState, BusServoState

pwm_servo_data_detection = False
running = True

def shutdown(signum, frame):
    global running
    running = False
    print('shutdown')
    rclpy.shutdown()

class BusServoControlNode(Node):
    def __init__(self):
        super().__init__('bus_servo_demo')
        self.bus_servo_pub = self.create_publisher(SetBusServoState, '/ros_robot_controller/bus_servo/set_position', 10)
        self.bus_servo_sub = self.create_subscription(SetBusServoState, '/ros_robot_controller/bus_servo/set_position', self.bus_servo_data_callback, 10)
        self.timer = self.create_timer(0.5, self.timer_callback)

    def bus_servo_data_callback(self, msg):
        global pwm_servo_data_detection
        print(msg)
        if msg.state[0].present_id != []:
            pwm_servo_data_detection = True

    def bus_servo_controls(self, id=0, position=0, offset=0, duration=0.0):
        bus_servo_data = SetBusServoState()
        data = BusServoState()
        data.present_id = [id]
        data.position = [position]
        data.offset = [offset]
        bus_servo_data.state = [data]
        bus_servo_data.duration = duration
        self.bus_servo_pub.publish(bus_servo_data)

    def timer_callback(self):
        self.bus_servo_controls(id=1, position=500, duration=1.0)
        self.get_clock().sleep_for(0.5)
        self.bus_servo_controls(id=1, position=1000, duration=1.0)
        self.get_clock().sleep_for(0.5)

def main(args=None):
    global running
    rclpy.init(args=args)
    signal.signal(signal.SIGINT, shutdown)

    node = BusServoControlNode()

    while running:
        rclpy.spin_once(node, timeout_sec=0.1)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

