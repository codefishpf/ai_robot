#!/usr/bin/env python3
# coding=utf-8
import os
import time
import rclpy
import threading
import subprocess
from rclpy.node import Node
from std_srvs.srv import Trigger
from std_msgs.msg import String, Bool
from rclpy.executors import MultiThreadedExecutor
from xf_mic_asr_offline_msgs.srv import GetOfflineResult
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from xf_mic_asr_offline.voice_play import play, set_default_device, set_default_language

SECONDS_PER_ORDER = 10


class ASRNode(Node):

    def __init__(self, name):
        rclpy.init()
        super().__init__(name)

        # 设置语音播放参数
        self.declare_parameter('audio_device', 'plughw:2,0')
        self.declare_parameter('language', 'Chinese')

        audio_device = self.get_parameter('audio_device').value
        language = self.get_parameter('language').value

        # 配置语音播放器
        set_default_device(audio_device)
        set_default_language(language)

        self.get_logger().info(
            f'Audio device: {audio_device}, Language: {language}')

        self.awake_flag = False
        self.recognize_fail_count = 0
        self.recognize_fail_count_threshold = 15
        # self.declare_parameter('confidence', 10)
        self.declare_parameter('confidence', 1)
        self.declare_parameter('seconds_per_order', SECONDS_PER_ORDER)

        self.confidence_threshold = self.get_parameter('confidence').value
        self.seconds_per_order = self.get_parameter('seconds_per_order').value

        self.control = self.create_publisher(String, '~/voice_words', 1)

        timer_cb_group = MutuallyExclusiveCallbackGroup()
        self._sub = self.create_subscription(Bool, '/awake_node/awake_flag',
                                             self.awake_flag_callback, 1)

        self.get_offline_result_client = self.create_client(
            GetOfflineResult, '/voice_control/get_offline_result')
        self.get_offline_result_client.wait_for_service()
        self.create_client(Trigger,
                           '/awake_node/init_finish').wait_for_service()

        self.create_timer(0.1, self.main, callback_group=timer_cb_group)
        self.create_service(Trigger, '~/init_finish', self.get_node_state)
        self.get_logger().info('\033[1;32m%s\033[0m' % 'start')

    def get_node_state(self, request, response):
        response.success = True
        return response

    def awake_flag_callback(self, msg):
        self.recognize_fail_count = 0
        self.awake_flag = msg.data

        if self.awake_flag:
            # 使用语音播放模块播放唤醒反馈
            self.get_logger().error('playok')
            play('ok')  # 播放 ok.wav 文件

            count_msg = String()
            count_msg.data = "唤醒成功(wake-up-success)"
            self.control.publish(count_msg)
            self.get_logger().info('\033[1;32m唤醒成功(wake-up-success)\033[0m')

    def main(self):
        if self.awake_flag:
            response = self.send_request()
            self.get_logger().info('\033[1;32mresult: %s\033[0m' %
                                   response.text)
            count_msg = String()
            if response.text == "休眠(Sleep)":  # 主动休眠(active sleep)
                self.awake_flag = 0
                count_msg.data = "休眠(Sleep)"
                self.recognize_fail_count = 0
                self.get_logger().info('\033[1;32m休眠(Sleep)\033[0m')
            elif response.result == "ok":  # 清零被动休眠相关变量(clear passive sleep relative variable)
                self.awake_flag = 0
                self.recognize_fail_count = 0
                count_msg.data = response.text
                self.control.publish(count_msg)
                self.get_logger().info('\033[1;32mok\033[0m')
            elif response.result == "fail":  # 记录识别失败次数(record the number of recognition failures)
                self.recognize_fail_count += 1
                if self.recognize_fail_count == 5:  # 连续识别失败5次，用户界面显示提醒信息(fail to recognize for consecutive 5 times.Warning occurs on user interface)
                    count_msg.data = "失败5次(Fail-5-times)"
                    self.control.publish(count_msg)
                    self.get_logger().info(
                        '\033[1;32m失败5次(Fail-5-times)\033[0m')
                elif self.recognize_fail_count == 10:  # 连续识别失败10次，用户界面显示提醒信息(fail to recognize for consecutive 10 times.Warning occurs on user interface)
                    count_msg.data = "失败10次(Fail-10-times)"
                    self.control.publish(count_msg)
                    self.get_logger().info(
                        '\033[1;32m失败10次(Fail-10-times)\033[0m')
                elif self.recognize_fail_count >= self.recognize_fail_count_threshold:  # 被动休眠(passive sleep)
                    self.awake_flag = 0
                    count_msg.data = "休眠(Sleep)"
                    self.control.publish(count_msg)
                    self.recognize_fail_count = 0
                    self.get_logger().info('\033[1;32m休眠(Sleep)\033[0m')

    def send_request(self):
        get_result_msg = GetOfflineResult.Request()
        get_result_msg.offline_recognise_start = 1
        get_result_msg.confidence_threshold = self.confidence_threshold
        get_result_msg.time_per_order = self.seconds_per_order
        self.get_logger().info('get_result_msg request: %s' % get_result_msg)
        self.future = self.get_offline_result_client.call_async(get_result_msg)
        while rclpy.ok():
            if self.future.done() and self.future.result():
                return self.future.result()
            time.sleep(0.01)


def main():
    node = ASRNode('asr_node')
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    executor.spin()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
