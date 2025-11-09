#!/bin/bash
# sync src code from local to pi

# 注意先将以下参数（机器人的name，ip，密码）写入.bashrc或.zshrc
# BOT_NAME='pi'
# BOT_IP='192.168.3.25'
# BOT_PASSWORD=''

echo "将本机的src拷贝到mentorpi (注意先将以下BOT_NAME和BOT_IP改成你树莓派的name,ip,password)"
echo "BOT_NAME: $BOT_NAME, BOT_IP: $BOT_IP, BOT_PASSWORD: $BOT_PASSWORD"
set -x
echo "1.备份mentorpi docker内的src到/home/pi/docker/tmp/src_copy_from_pi/"
sshpass -p $BOT_PASSWORD ssh $BOT_NAME@$BOT_IP "docker cp MentorPi:/home/ubuntu/ros2_ws/src /home/pi/docker/tmp/src_copy_from_pi/"
echo "2.将本机src拷贝到docker内 ros2_ws/src_from_local"
sshpass -p $BOT_PASSWORD scp -r $HOME/src/ai_robot/MentorPi/src $BOT_NAME@$BOT_IP:/home/pi/docker/tmp/src_from_local/
sshpass -p $BOT_PASSWORD ssh $BOT_NAME@$BOT_IP "ls -lht /home/pi/docker/tmp/src_from_local/"
sshpass -p $BOT_PASSWORD ssh $BOT_NAME@$BOT_IP "docker cp /home/pi/docker/tmp/src_from_local/src MentorPi:/home/ubuntu/ros2_ws/src_from_local/"
exit
echo "done"
