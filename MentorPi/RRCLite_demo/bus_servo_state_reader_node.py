import rclpy
from rclpy.node import Node
from ros_robot_controller_msgs.srv import GetBusServoState

class ServoStateSubscriber(Node):
    def __init__(self):
        super().__init__('servo_state_subscriber')
        # 创建服务客户端(create service client)
        self.srv_client = self.create_client(GetBusServoState, '/ros_robot_controller/bus_servo/get_state')

    def call_service(self):
        # 等待服务可用(wait for the service to become available)
        while not self.srv_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        request = GetBusServoState.Request()
        # 这里可以设置特定的请求参数，例如 request.ids = [servo_id_list](specific request parameters can be set, for example, request.ids = [servo_id_list])
        # 假设我们请求所有舵机的状态，不设置特定的参数(assume that the status of all servos are being request without setting specific parameters)
        future = self.srv_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        if future.result() is not None:
            if future.result().success:
                self.get_logger().info('Service call successful')
                # 处理返回的状态信息(process the state information of returning)
                for servo_state in future.result().state:
                    self.get_logger().info(
                        f'ID: {servo_state.id}, Position: {servo_state.position}')
            else:
                self.get_logger().info('Service call failed')

def main(args=None):
    rclpy.init(args=args)
    subscriber = ServoStateSubscriber()
    subscriber.call_service()  # 调用服务(callback service)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
