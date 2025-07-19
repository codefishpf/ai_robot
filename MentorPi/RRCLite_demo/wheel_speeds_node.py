import rclpy
from rclpy.node import Node
from ros_robot_controller_msgs.msg import WheelSpeeds

class WheelSpeedsSubscriber(Node):
    def __init__(self):
        super().__init__('wheel_speeds_subscriber')

        self.declare_parameter('wheel_speeds_topic', '/ros_robot_controller/wheel_speeds')
        self.wheel_speeds_topic = self.get_parameter('wheel_speeds_topic').get_parameter_value().string_value

        self.subscription = self.create_subscription(
            WheelSpeeds,
            self.wheel_speeds_topic,
            self.listener_callback,
            10)
        
        self.subscription  # prevent unused variable warning
        self.get_logger().info(f'Subscribed to {self.wheel_speeds_topic}')

    def listener_callback(self, msg):
        self.get_logger().info(f'Wheel speeds: {msg.wheel_speed_rps} rps')

def main(args=None):
    rclpy.init(args=args)
    node = WheelSpeedsSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
