import sys
import time
import signal
import threading
import ros_robot_controller_sdk as rrc

print('''
**********************************************************
********功能:幻尔科技树莓派扩展板，读取总线舵机数据(function:Hiwonder Raspberry Pi expansion board, read bus servo data)**********
**********************************************************
----------------------------------------------------------
官方网站(official website)：https://www.hiwonder.com
在线商城(online store)：https://hiwonder.tmall.com
----------------------------------------------------------
提示(tip)：
 * 按下Ctrl+C可关闭此次程序运行，若失败请多次尝试！(Press 'Ctrl+C' to exit this program. If it fails, please try again!)
----------------------------------------------------------
''')
board = rrc.Board()
board.enable_reception()
start = True

# 关闭前处理(processing before closing)
def Stop(signum, frame):
    global start
    start = False
    print('关闭中...')

signal.signal(signal.SIGINT, Stop)

def bus_servo_test(board):
    servo_id = board.bus_servo_read_id()
    servo_id = servo_id[0]
    vin =  board.bus_servo_read_vin(servo_id)
    temp = board.bus_servo_read_temp(servo_id)
    position = board.bus_servo_read_position(servo_id)
    # 输出舵机状态(output servo status)
    print("id:", servo_id)
    print('vin:', vin)
    print('temp:',temp)
    print('position',position)


if __name__ == '__main__':
    try:
        while start:
            bus_servo_test(board)
            time.sleep(1)
    except KeyboardInterrupt:
        print('强行退出')