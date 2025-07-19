#!/usr/bin/python3
# coding=utf8
# 阿克曼底盘运动学(Ackermann wheel chassis kinematic)
import math
from ros_robot_controller_msgs.msg import MotorState, MotorsState

class AckermannChassis:
    # wheelbase = 0.213  # 前后轴距(distance between front and real axles)
    # track_width = 0.222  # 左右轴距(distance between left and right axles)
    # wheel_diameter = 0.101  # 轮子直径(wheel diameter)

    def __init__(self, wheelbase=0.145, track_width=0.133, wheel_diameter=0.067):
        self.wheelbase = wheelbase
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

    def set_velocity(self, linear_speed, angular_speed, reset_servo=True):
        servo_angle = 1500
        data = []
        if abs(linear_speed) >= 1e-8:
            if abs(angular_speed) >= 1e-8:
                theta = math.atan(self.wheelbase*angular_speed/linear_speed)
                steering_angle = theta
                # print(math.degrees(steering_angle))
                if abs(steering_angle) > math.radians(29):
                    steering_angle = math.radians(29)
                    # for i in range(4):
                        # msg = MotorState()
                        # msg.id = i + 1
                        # msg.rps = 0.0
                        # data.append(msg)
                    # msg = MotorsState()
                    # msg.data = data
                    # return None, msg
                servo_angle = 1500 + 2000*math.degrees(-steering_angle)/180
   

            vr = linear_speed + angular_speed*self.track_width/2
            vl = linear_speed - angular_speed*self.track_width/2
            v_s = [self.speed_covert(v) for v in [0, vl, 0, -vr]]
            for i in range(len(v_s)):
                msg = MotorState()
                msg.id = i + 1
                msg.rps = float(v_s[i])
                data.append(msg) 
            msg = MotorsState()
            msg.data = data
            return servo_angle, msg
        else:
            for i in range(4):
                msg = MotorState()
                msg.id = i + 1
                msg.rps = 0.0
                data.append(msg)
            msg = MotorsState()
            msg.data = data
            return None, msg

    def get_velocity(self, wheel_speeds_rps):
        """
        Compute linear and angular speed from four wheel speeds
        :param wheel_speeds_rps:
        :return:
        """
        pass
