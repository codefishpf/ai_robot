import rclpy
from rclpy.node import Node
from ros_robot_controller_msgs.msg import MotorsState, MotorState

class MotorControlNode(Node):
    def __init__(self):
        super().__init__('motor_control_node')
        self.motor_pub = self.create_publisher(MotorsState, '/ros_robot_controller/set_motor', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        msg = MotorsState()
        motor_state = MotorState()
        motor_state.id = 2
        motor_state.rps = 0.2
        msg.data.append(motor_state)
        self.motor_pub.publish(msg)
        self.get_logger().info('Sent motor control message')

def main(args=None):
    rclpy.init(args=args)
    node = MotorControlNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

