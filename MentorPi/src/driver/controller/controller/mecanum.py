#!/usr/bin/python3
# coding=utf8
# 两轮差速驱动底盘运动学(Differential driven chassis kinematic)
import math
from ros_robot_controller_msgs.msg import MotorState, MotorsState

# Due to APP/UI can not support Mecanum and Ackerman,
# Hack Mecanum by Differential Driven.
class MecanumChassis:
    # track_width = 0.200 # 左右轴距(distance between left and right axles)
    # wheel_diameter = 0.067  # 轮子直径(wheel diameter)
    def __init__(self, track_width=0.200, wheel_diameter=0.067):
        self.track_width = track_width
        self.wheel_diameter = wheel_diameter

    def speed_covert(self, speed):
        """
        covert speed m/s to rps
        :param speed:
        :return:
        """
        # distance / circumference = rotations per second
        return speed / (math.pi * self.wheel_diameter)
    
    def wheel_speed_parse(self, wheel_speed_rps):
        """
        parse wheelspeed rps to m/s
        :param wheel speed rps:
        :return:
        """
        return wheel_speed_rps * (math.pi * self.wheel_diameter)

    def set_velocity(self, linear_speed, angular_speed):
        """
        Control moving
                    x
        v1 motor1|  ↑  |motor2 v2
          +  y - |     |
        :param linear_speed: m/s
        :param angular_speed:  yaw rate in rad/s
        :return:
        """
        vl = linear_speed - angular_speed*self.track_width/2
        vr = linear_speed + angular_speed*self.track_width/2
        v_s = [self.speed_covert(v) for v in [-vl, vr, 0, 0]]
        data = []
        for i in range(len(v_s)):
            msg = MotorState()
            msg.id = i + 1
            msg.rps = float(v_s[i])
            data.append(msg)

        msg = MotorsState()
        msg.data = data
        return msg
    
    def get_velocity(self, wheel_speeds_rps):
        """
        Compute linear and angular speed from four wheel speeds
        :param wheel_speeds_rps:
        :return:
        """
        wheel_speed_l = self.wheel_speed_parse(wheel_speeds_rps[0])
        wheel_speed_r = self.wheel_speed_parse(wheel_speeds_rps[1])
        linear_speed = (-wheel_speed_l + wheel_speed_r) / 2
        angular_speed = (wheel_speed_r - (-wheel_speed_l)) / self.track_width
        return linear_speed, angular_speed
