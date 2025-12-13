import os
from launch_ros.actions import Node
from launch import LaunchDescription, LaunchService
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument, OpaqueFunction

AWAKE_WORD = 'xiao3 ai4'


def launch_setup(context):
    # 安全获取环境变量并提供默认值
    mic_type = os.getenv('MIC_TYPE', 'xf')  # 默认使用 xf 麦克风
    asr_language = os.getenv('ASR_LANGUAGE', 'Chinese')  # 默认使用中文

    if mic_type == 'xf':
        # app id from zhaoxi
        # appid = LaunchConfiguration('appid', default="'86df9570'")
        appid = LaunchConfiguration('appid', default="'3a37c212'")
        # enable setting if you use a new wakeup word
        enable_setting = LaunchConfiguration('enable_setting', default='false')
        confidence = LaunchConfiguration(
            'confidence', default='18'
        )  # 语音识别结果自信度阈值，取值：0-100(voice recognition result confidence ranging from 0 to 100)
        seconds_per_order = LaunchConfiguration(
            'seconds_per_order', default='10'
        )  # 每次语音指令录音长度，单位：秒(recording length of each voice command in seconds)
        chinese_awake_words = LaunchConfiguration('chinese_awake_words',
                                                  default=AWAKE_WORD)
        english_awake_words = LaunchConfiguration('english_awake_words',
                                                  default='hello hi wonder')
        # language = LaunchConfiguration('language', default=os.environ['ASR_LANGUAGE']).perform(context)
        language = LaunchConfiguration('language',
                                       default=asr_language).perform(context)

        appid_arg = DeclareLaunchArgument('appid', default_value=appid)
        enable_setting_arg = DeclareLaunchArgument(
            'enable_setting', default_value=enable_setting)
        confidence_arg = DeclareLaunchArgument('confidence',
                                               default_value=confidence)
        seconds_per_order_arg = DeclareLaunchArgument(
            'seconds_per_order', default_value=seconds_per_order)
        chinese_awake_words_arg = DeclareLaunchArgument(
            'chinese_awake_words', default_value=chinese_awake_words)
        english_awake_words_arg = DeclareLaunchArgument(
            'english_awake_words', default_value=english_awake_words)
        language_arg = DeclareLaunchArgument('language',
                                             default_value=language)
        if language == 'Chinese':
            awake_words = chinese_awake_words
        else:
            awake_words = english_awake_words

        awake_node = Node(
            package="xf_mic_asr_offline",
            executable="awake_node.py",
            output='screen',
            parameters=[{
                "port": "/dev/ttyUSB0",
                "mic_type": "mic6_circle",
                "awake_word": awake_words,
                "enable_setting": enable_setting
            }],
        )

        asr_node = Node(
            package="xf_mic_asr_offline",
            executable="asr_node.py",
            output='screen',
            parameters=[{
                "confidence":
                confidence,
                "seconds_per_order":
                seconds_per_order,
                "feedback_audio":
                "/home/ubuntu/ros2_ws/src/xf_mic_asr_offline/feedback_voice/ok.wav"
            }],
            # huanjingbianliang
            env={
                'HOME': '/home/ubuntu',
                'ROS_HOME': '/home/ubuntu/.ros',
                'ROS_LOG_DIR': '/home/ubuntu/.ros/log',
                'LANG': 'en_US.UTF-8',
                'LC_ALL': 'en_US.UTF-8',
                'PATH': os.environ['PATH'],
                'PYTHONPATH': os.environ.get('PYTHONPATH', ''),
                'LD_LIBRARY_PATH': os.environ.get('LD_LIBRARY_PATH', ''),
                'ROS_DISTRO': os.environ.get('ROS_DISTRO', ''),
                'AMENT_PREFIX_PATH': os.environ.get('AMENT_PREFIX_PATH', ''),
                'COLCON_PREFIX_PATH': os.environ.get('COLCON_PREFIX_PATH', '')
            })

        install_lib_path = '/home/ubuntu/ros2_ws/install/xf_mic_asr_offline/lib/xf_mic_asr_offline'
        voice_control = Node(package="xf_mic_asr_offline",
                             executable="voice_control",
                             output='screen',
                             parameters=[{
                                 "appid":
                                 appid,
                                 "source_path":
                                 "/home/ubuntu/ros2_ws/src/xf_mic_asr_offline"
                             }],
                             env={
                                 'HOME':
                                 '/home/ubuntu',
                                 'ROS_LOG_DIR':
                                 '/home/ubuntu/.ros/log',
                                 'LD_LIBRARY_PATH':
                                 install_lib_path + ':' +
                                 os.environ.get('LD_LIBRARY_PATH', '')
                             })

        return [
            appid_arg,
            enable_setting_arg,
            confidence_arg,
            seconds_per_order_arg,
            chinese_awake_words_arg,
            english_awake_words_arg,
            language_arg,
            awake_node,
            voice_control,
            asr_node,
        ]
    else:
        awake_node = Node(
            package="xf_mic_asr_offline",
            executable="wonder_echo_pro_node.py",
            output='screen',
            parameters=[{
                "port": "/dev/ttyUSB0"
            }],
        )
        return [awake_node]


def generate_launch_description():
    return LaunchDescription([OpaqueFunction(function=launch_setup)])


if __name__ == '__main__':
    # 创建一个LaunchDescription对象(create a LaunchDescription object)
    ld = generate_launch_description()

    ls = LaunchService()
    ls.include_launch_description(ld)
    ls.run()
