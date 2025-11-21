#!/bin/bash
# sync src code from local to pi

# 配置变量 - 根据你的实际情况修改这些值
BOT_NAME='pi'
BOT_IP='192.168.149.1'
BOT_PASSWORD='raspberrypi'

# 路径配置
LOCAL_SRC_PATH="$HOME/Documents/AiRobot/ai_robot/MentorPi/src"
PI_BACKUP_PATH="/home/pi/docker/tmp/src_copy_from_pi"
PI_TEMP_PATH="/home/pi/docker/tmp/src_from_local"
DOCKER_CONTAINER_NAME="MentorPi"
DOCKER_WORKSPACE_PATH="/home/ubuntu/ros2_ws"

echo "将本机的src拷贝到mentorpi"
echo "BOT_NAME: $BOT_NAME, BOT_IP: $BOT_IP"
set -x

echo "0.在树莓派上创建必要的目录"
sshpass -p $BOT_PASSWORD ssh $BOT_NAME@$BOT_IP "mkdir -p $PI_BACKUP_PATH $PI_TEMP_PATH && echo '目录创建成功' && ls -la /home/pi/docker/tmp/"

# echo "1.备份mentorpi docker内的src到$PI_BACKUP_PATH/"
# sshpass -p $BOT_PASSWORD ssh $BOT_NAME@$BOT_IP "docker cp $DOCKER_CONTAINER_NAME:$DOCKER_WORKSPACE_PATH/src $PI_BACKUP_PATH/"

echo "2.将本机src拷贝到docker内 $DOCKER_WORKSPACE_PATH/src"
sshpass -p $BOT_PASSWORD scp -r $LOCAL_SRC_PATH $BOT_NAME@$BOT_IP:$PI_TEMP_PATH/
sshpass -p $BOT_PASSWORD ssh $BOT_NAME@$BOT_IP "ls -lht $PI_TEMP_PATH/"
sshpass -p $BOT_PASSWORD ssh $BOT_NAME@$BOT_IP "docker cp $PI_TEMP_PATH/src $DOCKER_CONTAINER_NAME:$DOCKER_WORKSPACE_PATH/src/"

set +x
echo "done"
