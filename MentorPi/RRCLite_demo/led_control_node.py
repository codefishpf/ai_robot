import rclpy
from rclpy.node import Node
from ros_robot_controller_msgs.msg import LedState

class LedControlNode(Node):
    def __init__(self):
        super().__init__('led_control_node')
        self.led_pub = self.create_publisher(LedState, '/ros_robot_controller/set_led', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        msg = LedState()
        msg.id = 1
        msg.on_time = 0.5
        msg.off_time = 0.5
        msg.repeat = 10
        self.led_pub.publish(msg)
        self.get_logger().info(f'Sent LED control message: id={msg.id}, on_time={msg.on_time}, off_time={msg.off_time}, repeat={msg.repeat}')

def main(args=None):
    rclpy.init(args=args)
    node = LedControlNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

