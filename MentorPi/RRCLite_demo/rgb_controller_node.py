#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from ros_robot_controller_msgs.msg import RGBState, RGBStates

class RGBControllerNode(Node):
    def __init__(self):
        super().__init__('rgb_controller')
        self.publisher_ = self.create_publisher(RGBStates, '/ros_robot_controller/set_rgb', 10)
        self.timer = self.create_timer(2.0, self.timer_callback)
        self.get_logger().info('RGB Controller Node has been started.')
        self.current_color_index = 0

    def timer_callback(self):
        # Define a set of colors
        colors = [
            (255, 0, 0),    # Red
            (0, 255, 0),    # Green
            (0, 0, 255),    # Blue
            (255, 255, 0),  # Yellow
            (0, 255, 255),  # Cyan
            (255, 0, 255)   # Magenta
        ]

        # Change the color for both LEDs
        color = colors[self.current_color_index % len(colors)]
        self.current_color_index += 1

        msg = RGBStates()
        msg.states = [
            RGBState(index=1, red=color[0], green=color[1], blue=color[2]),
            RGBState(index=2, red=color[0], green=color[1], blue=color[2])
        ]

        self.publisher_.publish(msg)
        self.get_logger().info(f'Setting LEDs to color R={color[0]}, G={color[1]}, B={color[2]}')

def main(args=None):
    rclpy.init(args=args)
    node = RGBControllerNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down RGB Controller Node')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

