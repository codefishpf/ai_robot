import rclpy
from rclpy.node import Node
from ros_robot_controller_msgs.msg import BuzzerState

class BuzzerControlNode(Node):
    def __init__(self):
        super().__init__('buzzer_control_node')
        self.buzzer_pub = self.create_publisher(BuzzerState, '/ros_robot_controller/set_buzzer', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        msg = BuzzerState()
        msg.freq = 1000
        msg.on_time = 0.5
        msg.off_time = 0.5
        msg.repeat = 5
        self.buzzer_pub.publish(msg)
        self.get_logger().info(f'Sent buzzer control message: freq={msg.freq}, on_time={msg.on_time}, off_time={msg.off_time}, repeat={msg.repeat}')

def main(args=None):
    rclpy.init(args=args)
    node = BuzzerControlNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

