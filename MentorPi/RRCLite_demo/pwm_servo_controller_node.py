#!/usr/bin/env python3
# encoding: utf-8

import rclpy
from rclpy.node import Node
from ros_robot_controller_msgs.msg import SetPWMServoState, PWMServoState

class PWMServoController(Node):
    def __init__(self):
        super().__init__('pwm_servo_controller')
        
        self.declare_parameter('servo_id', 3)
        self.declare_parameter('initial_position', 500)
        self.declare_parameter('offset', 0)
        self.declare_parameter('step_size', 1000)
        self.declare_parameter('timer_interval', 0.5)
        
        self.servo_id = self.get_parameter('servo_id').get_parameter_value().integer_value
        self.initial_position = self.get_parameter('initial_position').get_parameter_value().integer_value
        self.offset = self.get_parameter('offset').get_parameter_value().integer_value
        self.step_size = self.get_parameter('step_size').get_parameter_value().integer_value
        self.timer_interval = self.get_parameter('timer_interval').get_parameter_value().double_value
        
        self.publisher = self.create_publisher(SetPWMServoState, '/ros_robot_controller/pwm_servo/set_state', 10)
        
        self.timer = self.create_timer(self.timer_interval, self.timer_callback)
        
        self.position = self.initial_position
        self.direction = 1

        self.set_servo_position(self.initial_position)

    def set_servo_position(self, position):
        msg = SetPWMServoState()
        servo_state = PWMServoState()
        servo_state.id = [self.servo_id]
        servo_state.position = [position]
        servo_state.offset = [self.offset]
        
        msg.state.append(servo_state)
        
        self.publisher.publish(msg)
        self.get_logger().info(f'Sent position {position} to servo {self.servo_id}')

    def timer_callback(self):
        self.position += self.direction * self.step_size
        if self.position >= 2500 or self.position <= 500:
            self.direction *= -1
            self.position = max(500, min(self.position, 2500))
        self.set_servo_position(self.position)

def main(args=None):
    rclpy.init(args=args)
    node = PWMServoController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

