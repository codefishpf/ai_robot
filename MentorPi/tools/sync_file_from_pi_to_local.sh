#!/bin/bash

# 注意先将以下参数（机器人的name，ip，密码）写入.bashrc或.zshrc
# BOT_NAME='pi'
# BOT_IP='192.168.3.25'
# BOT_PASSWORD=''

echo "将树莓派docker内的指定文件拷贝到本机"
# 需要带完整源路径和目标路径
# 例如：bash sync_file_from_pi_to_local.sh rtabmap.db /home/ubuntu/.ros/rtabmap.db /Users/chenxu/tmp_robot_file
echo "BOT_NAME: $BOT_NAME, BOT_IP: $BOT_IP, BOT_PASSWORD: $BOT_PASSWORD"
echo "源路径：$1, 目标路径：$2"
set -x
sshpass -p $BOT_PASSWORD ssh $BOT_NAME@$BOT_IP "docker cp MentorPi:$1 /home/pi/docker/tmp/tmp_file_from_pi.tar"
sshpass -p $BOT_PASSWORD scp $BOT_NAME@$BOT_IP:/home/pi/docker/tmp/tmp_file_from_pi.tar $2
ls -lht $2
exit
echo "done"
