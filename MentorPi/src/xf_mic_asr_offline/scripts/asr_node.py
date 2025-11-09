#!/usr/bin/env python3
# coding=utf-8
# @Author: Aiden
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


class ASRNode(Node):

    def __init__(self, name):
        rclpy.init()
        super().__init__(name)

        # 新增参数：音频文件路径 7/12
        self.declare_parameter(
            'feedback_audio',
            '/home/ubuntu/ros2_ws/src/xf_mic_asr_offline/feedback_voice/ok.wav'
        )
        self.feedback_audio = self.get_parameter('feedback_audio').value
        self.get_logger().info(f'Feedback audio set to: {self.feedback_audio}')

        self.awake_flag = False
        self.recognize_fail_count = 0
        self.recognize_fail_count_threshold = 15
        self.declare_parameter('confidence', 18)
        self.declare_parameter('seconds_per_order', 5)

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
            # 在独立线程中播放音频，避免阻塞主线程
            threading.Thread(target=self.play_feedback_audio,
                             daemon=True).start()

            #            self.play('ok')

            count_msg = String()
            count_msg.data = "唤醒成功(wake-up-success)"
            self.control.publish(count_msg)
            self.get_logger().info('\033[1;32m唤醒成功(wake-up-success)\033[0m')

        # count_msg = String()
        # count_msg.data = "唤醒成功(wake-up-success)"
        # self.control.publish(count_msg)
        # self.get_logger().info('\033[1;32m唤醒成功(wake-up-success)\033[0m')

        # 新增函数：播放音频反馈 7/12
    def play_feedback_audio(self):
        """播放指定的音频文件作为唤醒反馈"""
        try:
            # 使用aplay播放WAV文件
            subprocess.run(['aplay', self.feedback_audio], check=True)
            self.get_logger().info(f'成功播放反馈音频: {self.feedback_audio}')
        except subprocess.CalledProcessError as e:
            self.get_logger().error(f'播放音频失败: {e}')
        except FileNotFoundError:
            self.get_logger().error(f'未找到音频文件: {self.feedback_audio}')
        except Exception as e:
            self.get_logger().error(f'播放音频时发生错误: {e}')


#    def play(self, name):
#        voice_play.play(name, language=self.language)

    def play_feedback_audio(self):
        try:
            self.get_logger().info(f'play audio: {self.feedback_audio}')

            if not os.path.isfile(self.feedback_audio):
                self.get_logger().error(
                    f'audio file not exist: {self.feedback_audio}')
                return

            if not os.access(self.feedback_audio, os.R_OK):
                self.get_logger().error(
                    f'file not read: {self.feedback_audio}')
                return

            self.get_logger().info(f'file play')

            result = subprocess.run(['aplay', self.feedback_audio],
                                    check=True,
                                    capture_output=True,
                                    text=True)
            self.get_logger().info(f'play successed: {self.feedback_audio}')

        except subprocess.CalledProcessError as e:
            self.get_logger().error(f'play failed: {e}')
            self.get_logger().error(f'error: {e.stderr}')
        except FileNotFoundError:
            self.get_logger().error(f'aplay alsa-utils')
        except Exception as e:
            self.get_logger().error(f'error occurred: {e}')

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
