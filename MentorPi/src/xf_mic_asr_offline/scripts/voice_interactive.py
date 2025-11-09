#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 语音控制移动(voice movement control)
import os
import json
import math
import time
import rclpy
import threading
import tf_transformations  # TF坐标变换库
import numpy as np
import sdk.pid as pid
import sdk.common as common
from rclpy.node import Node
from std_srvs.srv import Trigger
from geometry_msgs.msg import Twist, PoseStamped, PoseWithCovarianceStamped
from std_msgs.msg import String, Int32
from tf2_ros.buffer import Buffer
from tf2_ros import TransformException
from tf2_ros.transform_listener import TransformListener
from xf_mic_asr_offline.voice_play import play
from ros_robot_controller_msgs.msg import BuzzerState
from rclpy.qos import QoSProfile, QoSReliabilityPolicy

CAR_WIDTH = 0.4  # meter
DEFAULT_MOVE = 0.5  # meter


class VoiceInteractiveNode(Node):

    def __init__(self, name):
        rclpy.init()
        super().__init__(name)

        self.angle = None
        self.words = None
        self.running = True
        self.haved_stop = False
        self.current_pose = None
        self.start_follow = False
        self.last_status = Twist()
        self.threshold = 3
        self.speed = 0.3
        self.stop_dist = 0.4
        self.count = 0
        self.scan_angle = math.radians(90)

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.pid_yaw = pid.PID(1.6, 0, 0.16)
        self.pid_dist = pid.PID(1.7, 0, 0.16)

        self.language = os.environ['ASR_LANGUAGE']
        self.machine_type = os.environ.get('MACHINE_TYPE')
        self.mecanum_pub = self.create_publisher(Twist, '/controller/cmd_vel',
                                                 1)
        self.buzzer_pub = self.create_publisher(
            BuzzerState, '/ros_robot_controller/set_buzzer', 1)
        self.goal_pose_pub = self.create_publisher(PoseStamped, '/goal_pose',
                                                   1)
        qos = QoSProfile(depth=1, reliability=QoSReliabilityPolicy.BEST_EFFORT)
        #        self.create_subscription(LaserScan, '/scan_raw', self.lidar_callback, qos)  # 订阅雷达数据(subscribe to Lidar data)
        self.create_subscription(String, '/asr_node/voice_words',
                                 self.words_callback, 1)
        self.create_subscription(Int32, '/awake_node/angle',
                                 self.angle_callback, 1)
        # self.pose_sub = self.create_subscription(PoseWithCovarianceStamped,
        #                                          'set_pose',
        #                                          self.pose_callback, 1)

        self.client = self.create_client(Trigger, '/asr_node/init_finish')
        self.client.wait_for_service()  # 阻塞等待(blocking wait)
        self.declare_parameter('delay', 0)
        time.sleep(self.get_parameter('delay').value)
        self.mecanum_pub.publish(Twist())
        self.play('running')

        self.get_logger().info('唤醒口令: 小艾(Wake up word: hello hiwonder)')
        self.get_logger().info(
            '唤醒后15秒内可以不用再唤醒(No need to wake up within 15 seconds after waking up)'
        )
        self.get_logger().info(
            '控制指令: 左转 右转 前进 后退 过来(Voice command: turn left/turn right/go forward/go backward/come here)'
        )
        self.stop_time_stamp = time.time()
        self.current_time_stamp = time.time()
        threading.Thread(target=self.main, daemon=True).start()
        self.create_service(Trigger, '~/init_finish', self.get_node_state)
        self.get_logger().info('\033[1;32m%s\033[0m' % 'start')

    def get_node_state(self, request, response):
        response.success = True
        return response

    def play(self, name):
        play(name, language=self.language)

    def words_callback(self, msg):
        #self.words = json.dumps(msg.data, ensure_ascii=False)[1:-1]
        self.words = msg.data
        if self.language == 'Chinese':
            self.words = self.words.replace(' ', '')
        self.get_logger().info('words:%s' % self.words)
        if self.words is not None and self.words not in [
                '唤醒成功(wake-up-success)', '休眠(Sleep)', '失败5次(Fail-5-times)',
                '失败10次(Fail-10-times'
        ]:
            pass
        elif self.words == '唤醒成功(wake-up-success)':
            self.play('awake')
            pass
        elif self.words == '休眠(Sleep)':
            msg = BuzzerState()
            msg.freq = 1000
            msg.on_time = 0.1

            msg.off_time = 0.01
            msg.repeat = 1
            self.buzzer_pub.publish(msg)

    def angle_callback(self, msg):
        self.angle = msg.data
        self.get_logger().info('angle:%s' % self.angle)
        self.start_follow = False
        # self.mecanum_pub.publish(Twist())

    def get_current_pose(self):
        self.get_logger().info('get current pose from tf')
        try:
            now = rclpy.time.Time()  # 获取ROS系统的当前时间
            trans = self.tf_buffer.lookup_transform(  # 监听当前时刻源坐标系到目标坐标系的坐标变换
                'base_link', 'map', now)
        except TransformException as ex:  # 如果坐标变换获取失败，进入异常报告
            self.get_logger().info('Could not get transform, %s', ex)
        pos = trans.transform.translation  # 获取位置信息
        quat = trans.transform.rotation  # 获取姿态信息（四元数）
        euler = tf_transformations.euler_from_quaternion(
            [quat.x, quat.y, quat.z, quat.w])
        self.get_logger().info(
            'Get %s --> %s transform: [%f, %f, %f] [%f, %f, %f]' %
            (self.source_frame, self.target_frame, pos.x, pos.y, pos.z,
             euler[0], euler[1], euler[2]))

    def compute_goal_pose(self):
        pose = PoseStamped()
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.header.frame_id = 'map'
        self.current_pose = self.get_current_pose()
        if not self.current_pose:
            self.get_logger().error('None current pose')
        if not self.angle:
            self.get_logger().error('None angle')
        angle_rad = math.radians(self.angle)
        pose.pose.position.x = self.current_pose.position.x + DEFAULT_MOVE * math.cos(
            angle_rad)
        pose.pose.position.y = self.current_pose.position.y + DEFAULT_MOVE * math.sin(
            angle_rad)
        pose.pose.position.z = 0.0
        pose.pose.orientation.x = 0.0
        pose.pose.orientation.y = 0.0
        pose.pose.orientation.z = 0.0
        self.get_logger().info('complete goal pose computaion: %s' % pose)
        return pose

    def main(self):
        while True:
            if self.words is not None:
                self.get_logger().info('move by words: %s' % self.words)
                self.get_logger().info('voice angle: %s' % self.angle)
                twist = Twist()
                if self.words == '前进' or self.words == 'goforward':
                    self.play('go')
                    self.stop_time_stamp = time.time() + 4
                    twist.linear.x = 0.2
                elif self.words == '后退' or self.words == 'gobackward':
                    self.play('back')
                    self.get_logger().info('Executing backward command')
                    self.stop_time_stamp = time.time() + 4
                    twist.linear.x = -0.2
                elif self.words == '左转' or self.words == 'turnleft':
                    self.play('turn_left')
                    self.stop_time_stamp = time.time() + 2
                    twist.angular.z = 0.8
                elif self.words == '右转' or self.words == 'turnright':
                    self.play('turn_right')
                    self.stop_time_stamp = time.time() + 2
                    twist.angular.z = -0.8
                elif self.words == '过来' or self.words == 'comehere':
                    self.play('come')
                    # if 270 > self.angle > 90:
                    #     twist.angular.z = -1.0
                    #     self.stop_time_stamp = time.time() + abs(
                    #         math.radians(self.angle - 90) / twist.angular.z)
                    # else:
                    #     twist.angular.z = 1.0
                    #     if self.angle <= 90:
                    #         self.angle = 90 - self.angle
                    #     else:
                    #         self.angle = 450 - self.angle
                    #     self.stop_time_stamp = time.time() + abs(
                    #         math.radians(self.angle) / twist.angular.z)

                    goal_pose = self.compute_goal_pose()
                    self.goal_pose_pub.publish(goal_pose)
                    # self.lidar_follow = True
                elif self.words == '休眠(Sleep)':
                    time.sleep(0.01)
                self.get_logger().info('to pub twist')
                self.words = None
                self.haved_stop = False
                self.mecanum_pub.publish(twist)
                self.get_logger().info('after pub twist')
            else:
                time.sleep(1.0)
            self.current_time_stamp = time.time()
            # 达到终止时间且小车还没停，就停止
            if self.stop_time_stamp < self.current_time_stamp and not self.haved_stop:
                self.get_logger().info('To stop a moving car')
                self.mecanum_pub.publish(Twist())
                self.haved_stop = True
            # if self.lidar_follow:
            #     self.lidar_follow = False
            #     self.start_follow = True


def main():
    node = VoiceInteractiveNode('voice_interactive')
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
