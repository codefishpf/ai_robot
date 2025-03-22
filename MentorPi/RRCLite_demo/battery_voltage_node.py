import rclpy
from rclpy.node import Node
from std_msgs.msg import UInt16

class BatteryVoltageSubscriberNode(Node):
    def __init__(self):
        super().__init__('battery_voltage_subscriber_node')
        self.subscription = self.create_subscription(
            UInt16,  
            '/ros_robot_controller/battery',  
            self.battery_voltage_callback, 
            10  #
        )
        self.subscription  

    def battery_voltage_callback(self, msg):
        self.get_logger().info(f'Received battery voltage: {msg.data} mV')

def main(args=None):
    rclpy.init(args=args)
    node = BatteryVoltageSubscriberNode()
    try:
        rclpy.spin(node)  
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
