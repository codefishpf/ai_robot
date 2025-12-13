#!/bin/bash

# 注意先将以下参数（机器人的name，ip，密码）写入.bashrc或.zshrc
# BOT_NAME='pi'
# BOT_IP='192.168.3.25'
# BOT_PASSWORD=''

echo "将本机的指定文件拷贝到mentorpi docker container内(注意先将以下BOT_NAME和BOT_IP改成你树莓派的name,ip,password)"
# 需要带完整路径和目标文件名
# 例如：bash sync_file_from_local_to_pi.sh /Users/chenxu/src/ai_robot/MentorPi/src/xf_mic_asr_offline/scripts/voice_interactive.py voice_interactive.py
echo "BOT_NAME: $BOT_NAME, BOT_IP: $BOT_IP, BOT_PASSWORD: $BOT_PASSWORD"
echo "文件路径：$1, 文件名：$2"
set -x
echo "1.将目标文件拷贝到/home/pi/docker/tmp/ 路径下"
sshpass -p $BOT_PASSWORD scp $1 $BOT_NAME@$BOT_IP:/home/pi/docker/tmp/$2
sshpass -p $BOT_PASSWORD ssh $BOT_NAME@$BOT_IP "ls -lht /home/pi/docker/tmp/"
echo "2.将目标文件拷贝到docker中的HOME路径下"
sshpass -p $BOT_PASSWORD ssh $BOT_NAME@$BOT_IP "docker cp /home/pi/docker/tmp/$2 MentorPi:/home/ubuntu/"
exit
echo "done"
