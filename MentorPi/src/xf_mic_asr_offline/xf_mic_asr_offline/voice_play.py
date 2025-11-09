#!/usr/bin/env python3
# encoding: utf-8
import os
import subprocess
import threading


class VoicePlayer:

    def __init__(self,
                 audio_device='plughw:2,0',
                 default_volume=80,
                 default_language='Chinese'):
        self.audio_device = audio_device
        self.default_volume = default_volume
        self.default_language = default_language
        self.wav_path = '/home/ubuntu/ros2_ws/src/xf_mic_asr_offline/feedback_voice'

    def get_audio_path(self, voice_name, language=None):
        """获取音频文件路径"""
        if language is None:
            language = self.default_language

        if language == 'Chinese':
            return os.path.join(self.wav_path, voice_name + '.wav')
        else:
            return os.path.join(self.wav_path, 'english', voice_name + '.wav')

    def play(self, voice_name, volume=None, language=None, async_play=True):
        """
        播放语音文件
        
        Args:
            voice_name: 语音文件名（不带扩展名）
            volume: 音量（0-100），如果为None则使用默认音量
            language: 语言，如果为None则使用默认语言
            async_play: 是否异步播放（不阻塞主线程）
        """
        if volume is None:
            volume = self.default_volume

        audio_file = self.get_audio_path(voice_name, language)

        if async_play:
            # 在独立线程中播放，避免阻塞主线程
            thread = threading.Thread(target=self._play_audio,
                                      args=(audio_file, volume),
                                      daemon=True)
            thread.start()
        else:
            # 同步播放（阻塞）
            self._play_audio(audio_file, volume)

    def _play_audio(self, audio_file, volume):
        """实际播放音频的内部方法"""
        try:
            # 设置音量（如果需要）
            # os.system(f'amixer -q -D pulse set Master {volume}%')

            # 使用aplay播放音频
            subprocess.run(['aplay', '-D', self.audio_device, audio_file],
                           check=True,
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL,
                           timeout=5)

        except subprocess.CalledProcessError as e:
            print(f'音频播放失败: {e}')
        except subprocess.TimeoutExpired:
            print('音频播放超时')
        except FileNotFoundError:
            print(f'音频文件未找到: {audio_file}')
        except Exception as e:
            print(f'播放音频时发生错误: {e}')


# 创建全局实例
default_player = VoicePlayer()


# 便捷函数
def play(voice_name, volume=None, language=None, async_play=True):
    """便捷函数，使用默认播放器播放音频"""
    default_player.play(voice_name, volume, language, async_play)


def set_default_device(device):
    """设置默认音频设备"""
    default_player.audio_device = device


def set_default_volume(volume):
    """设置默认音量"""
    default_player.default_volume = volume


def set_default_language(language):
    """设置默认语言"""
    default_player.default_language = language


if __name__ == '__main__':
    # 测试代码
    play('ok')
    play('running', language="English")
    play('running')
