#!/bin/bash
# sync src code from pi to local

# 注意先将以下参数（机器人的name，ip，密码）写入.bashrc或.zshrc
# BOT_NAME='pi'
# BOT_IP='192.168.3.25'
# BOT_PASSWORD=''

echo "将mentorpi上的src拷贝到本机"
echo "BOT_NAME: $BOT_NAME, BOT_IP: $BOT_IP, BOT_PASSWORD: $BOT_PASSWORD"

set -x
echo "输入树莓派密码..."
sshpass -p $BOT_PASSWORD ssh $BOT_NAME@$BOT_IP "ls -lht"
sshpass -p $BOT_PASSWORD docker cp MentorPi:/home/ubuntu/ros2_ws/src /home/pi/docker/tmp/src_copy_from_pi/
sshpass -p $BOT_PASSWORD scp -r $BOT_NAME@$BOT_IP:/home/pi/docker/tmp/src_copy_from_pi/src $HOME/src/ai_robot/MentorPi/src_copy_from_pi/
exit
echo "done"
