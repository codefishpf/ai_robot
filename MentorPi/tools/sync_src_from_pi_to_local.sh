#!/bin/bash
# sync src code from pi to local
echo "将mentorpi上的src拷贝到本机 (注意先将以下BOT_NAME和BOT_IP改成你树莓派的name和ip)"
BOT_NAME='pi'
BOT_IP='192.168.3.25'
set -x
echo "输入树莓派密码..."
ssh $BOT_NAME@$BOT_IP "ls"
ssh $BOT_NAME@$BOT_IP "ls -lht"
docker cp MentorPi:/home/ubuntu/ros2_ws/src /home/pi/docker/tmp/src_copy
exit
scp $BOT_NAME@$BOT_IP:/home/pi/docker/tmp/src_copy $HOME/src/ai_robot/MentorPi/
echo "done"
