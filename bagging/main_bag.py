import copy
import math
import time
import sys
from calendar import c
from operator import mod
import numpy as np
from ctypes import *
import time
import cv2
import copy
import darknet
import pyrealsense2 as rs
import rospy

# test123

sys.path.append("/home/hualen/Desktop/bagging")
# import YOLO_Detect
sys.path.append("/home/hualen/ax12_control")
from Ax12 import Ax12
import ax12move as mm 

so_file = "/home/hualen/Desktop/bagging/Hiwin_API.so"
modbus = CDLL(so_file)

Point_home = [ 0  , 368.000, 293.500, -180.000, 0.000, 90.000]
Point_Dist = [ 0  , 0.0, 0.0, -180.000, 0.0, 90.000]
Angel_Dist = [ 0  ,  0, -0, 0, 9, -0]
Angel_home = [ 0  ,  -0, -0, -0, -90, -0]

"""
    YOLO & Python 環境需求
        1. .data
        2. .name
        3. .cfg
        4. .weight
        5. darknet(shared library)
        6. darknet.py
        7. libdarknet.so
"""

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
pipeline.start(config)
sensor = pipeline.get_active_profile().get_device().query_sensors()[1]
sensor.set_option(rs.option.auto_exposure_priority, True)





# 手臂移動速度
speed_setting = 100  
acceleration_setting = 100




'''
    DO(int DO_Num, int x)                                                         # 1 -> on ; 0 -> off                                          
    HOME(int state)                                                               # 1 RUN
    PTP(int type, int vel, int acc, int TOOL, int BASE, double *Angle)            # 0 -> joint ; 1 -> coordinate
    LIN(int type,double *XYZ, int vel, int acc, int TOOL, int BASE)               # 0 -> joint ; 1 -> coordinate
    CIRC(double *CIRC_s, double *CIRC_end, int vel, int acc, int TOOL, int BASE) 
    JOG(int joint,int dir)
'''



'''
    手臂移動
'''


def arm_move(mode, speed ,acceleration):
    if mode=='PTP':
        PTP_Move(Point_Dist, speed, acceleration)   
    else:
        LIN_Move(Point_Dist, speed, acceleration)
    
    Point_now = copy.deepcopy(Point_Dist)


# Move PTP
def PTP_Move(Point, speed ,acceleration):
    print("... PTP Move ... " )
    C_PTP_XYZ = (c_double * len(Point))(*Point)         # C Array
    modbus.PTP(1, speed, acceleration, 0, 0, C_PTP_XYZ)
    modbus.Arm_State_REGISTERS()
    while 1:
        modbus.PTP(1, speed, acceleration, 0                                                       , 0, C_PTP_XYZ)
        print('======================================')
        print('modbus= ',modbus.Arm_State_REGISTERS())
        print('======================================')
        if(modbus.Arm_State_REGISTERS() == 1):
            break
    # if(modbus.Arm_State_REGISTERS() == 1):
    #     modbus.R200()
            
    print("END PTP Move!" )

# Move LIN   
def LIN_Move(Point, speed, acceleration):
    print("... LIN Move ... " )
    C_LIN_XYZ = (c_double * len(Point))(*Point)         # C Array
    modbus.LIN(1, speed, acceleration, 0, 0, C_LIN_XYZ)
    while 1:
        # frames = pipeline.wait_for_frames()         # 不斷更新Realsense預防模糊
        # frames.get_color_frame()                    # 同上
        modbus.LIN(1, speed, acceleration, 1, 0, C_LIN_XYZ)
        print('======================================')
        print('modbus= ',modbus.Arm_State_REGISTERS())
        print('======================================')
        if(modbus.Arm_State_REGISTERS() == 1):
            print(modbus.Arm_State_REGISTERS())
            break
        # time.sleep(0.01)
    print("END LIN Move!")

def Angel_Move(Point, speed, acceleration):
    print("... Angle Move ... " )
    C_PTP_XYZ = (c_double * len(Point))(*Point)         # C Array
    modbus.PTP(0, speed, acceleration, 0, 0, C_PTP_XYZ)
    modbus.Arm_State_REGISTERS()
    while 1:
        modbus.PTP(0, speed, acceleration, 0, 0, C_PTP_XYZ)
        print('======================================')
        print('modbus= ',modbus.Arm_State_REGISTERS())
        print('======================================')
        if(modbus.Arm_State_REGISTERS() == 1):
            break
    # if(modbus.Arm_State_REGISTERS() == 1):
    #     modbus.R200()
            
    print("END Angel Move!" )



'''
    拍照
'''
def get_picture():
    # img = cv2.imread("/home/weng/Downloads/15934122612690.jpg")
    print("Start Get Photo")
    frames = pipeline.wait_for_frames()
    img = frames.get_color_frame()
    img = np.asanyarray(img.get_data())
    print("Finish Get Photo")
    return img


"""
    motor setting
"""
# e.g 'COM3' windows or '/dev/ttyUSB0' for Linux /dev/motor_USB
Ax12.DEVICENAME = '/dev/ttyUSB0'
Ax12.BAUDRATE = 1_000_000
Ax12.DEBUG = True
# sets baudrate and opens com port
Ax12.connect()

# create AX12 instance with ID 10 
motor_id = 1
my_dxl = Ax12(motor_id)  
my_dxl.set_moving_speed(100)
my_dxl.print_status




if __name__ == "__main__":

    '''
        手臂設定
    '''
    Arm_statePTP = 0
    modbus.DO.argtypes = [c_int, c_int]
    modbus.PTP.argtypes = [c_int, c_int, c_int, c_int, c_int]
    modbus.LIN.argtypes = [c_int, c_int, c_int, c_int, c_int]
    modbus.libModbus_Connect()
    modbus.Holding_Registers_init()

    # '''
    #     吸嘴設定
    # '''
    IO_Port = 301 # D0
    command = 200

    # modbus.DO(301,0) # 1 -> on ; 0 -> off
    # modbus.DO(303PTP_Angel,0) # 1 -> on ; 0 -> off
    
    mm.motor_move(my_dxl,191)
    mm.motor_move(my_dxl,505)
    while 1 :
        key = input("Is ok? :")
        if key == 'a':
            break
        else :
            mm.motor_move(my_dxl,191)
            mm.motor_move(my_dxl,505)
            continue   
    #///////////////////////////////////////////////////////////
    Point_Dist = Point_home
    PTP_Move(Point_Dist, speed_setting ,acceleration_setting)
    Point_Dist = [0 , 242.741, 334.840, -180, 0, 90]
    PTP_Move(Point_Dist, speed_setting ,acceleration_setting)

    out_img = get_picture()
    cv2.imshow('out2', out_img)
    cv2.waitKey(10)
    time.sleep(3)
    
    """
    
        訂單1
    
    """
#拿取紙袋-放置工作區
    Point_Dist = [283.899, 258.249, 150, -180, 0, 90] #吸取紙袋位置
    arm_move('PTP',speed_setting,acceleration_setting)
    
    Point_Dist = [283.899, 258.249, 45.262, -180, 0, 90] #吸取紙袋位置
    arm_move('LIN',2000,100)

    modbus.DO(300,1)
    modbus.DO(303,1)

    Point_Dist = [355.673, 258.249, 254.912, -180, 0, 90] #抽出紙袋
    arm_move('PTP',speed_setting,acceleration_setting)

    Point_Dist = [82.692, 536.223, 254.912, -180, 0, 90] #到卡扣區
    arm_move('PTP',speed_setting,acceleration_setting)

    Point_Dist = [82.692, 536.223, 82.5, -180, 0, 90] #貼齊地面
    arm_move('LIN',2000,100)

    Point_Dist = [254.223, 532.223, 82.5, -180, 0, 90] #進入卡扣
    arm_move('LIN',2000,100)

    Point_Dist = [254.223, 532.223, 235.287, -180, 0, 90] #開袋
    arm_move('LIN',2000,100)

    Point_Dist = [-9.467, 532.223, 235.287, -180, 0, 90] #離開卡扣
    arm_move('LIN',2000,100)

    Point_Dist = [0.467, 532.223, 269.987, -180, 0, 90] #原地抬高
    arm_move('PTP',speed_setting,acceleration_setting)

    #轉伺服馬達
    mm.motor_move(my_dxl,191)
    

    Point_Dist = [-9.467, 532.223, 177.237, -180, 0, 90] #貼齊桌面
    arm_move('PTP',speed_setting,acceleration_setting)

    modbus.DO(300,0)
    modbus.DO(303,0)

    Point_Dist = [-9.467, 532.223, 235.612, -180, 0, 90] #原地抬高
    arm_move('PTP',speed_setting,acceleration_setting)


   



#商品(鐵鋁罐)
    Point_Dist = [-91.154, 364.887, 235.612, -180, 0, 90] #到商品上方
    arm_move('PTP',speed_setting,acceleration_setting)

    #轉伺服馬達
    mm.motor_move(my_dxl,505)

    Point_Dist = [-91.154, 364.887, 98.852, -180, 0, 90] #吸取商品
    arm_move('PTP',speed_setting,acceleration_setting)

    modbus.DO(300,1)
    modbus.DO(303,1)

    Point_Dist = [-91.154, 364.887, 344.602, -180, 0, 90] #原地抬高
    arm_move('PTP',speed_setting,acceleration_setting)

    Point_Dist = [86.364, 517.908, 344.602, -180, 0, 90] #到袋口
    arm_move('PTP',speed_setting,acceleration_setting)

    Point_Dist = [87.364, 517.908, 192.639, -180, 0, 90] #到袋口
    arm_move('LIN',2000,100)

    Point_Dist = [87.364, 582.766, 192.639, -180, 0, 90] #到袋口
    arm_move('LIN',2000,100)


    Point_Dist = [87.364, 582.766, 96.277, -180, 0, 90] #放入商品
    arm_move('LIN',2000,100)

    modbus.DO(300,0)
    modbus.DO(303,0)

    Point_Dist = [87.364, 582.766, 254.922, -180, 0, 90] #原地抬高
    arm_move('LIN',2000,100)


     #商品2-1(麥香)
    Point_Dist = [-150.667, 343.133, 254.922, -180, 0, 90] #到商品上方
    arm_move('PTP',speed_setting,acceleration_setting)

    Point_Dist = [-150.667, 343.133, 78.887, -180, 0, 90] #吸取商品
    arm_move('PTP',speed_setting,acceleration_setting)

    modbus.DO(300,1)
    modbus.DO(303,1)

    Point_Dist = [-150.667, 343.133, 322.662, -180, 0, 90] #原地抬高
    arm_move('PTP',speed_setting,acceleration_setting)

    Point_Dist = [90.054, 527.898, 322.662, -180, 0, 90] #到袋口
    arm_move('PTP',speed_setting,acceleration_setting)

    Point_Dist = [95.054, 527.898, 200.073, -180, 0, 90] #旋轉商品
    arm_move('PTP',speed_setting,acceleration_setting)

    Point_Dist = [95.054, 442.722, 200.073, -180, 0, -0.4] #旋轉商品
    arm_move('LIN',2000,100)

    Point_Dist = [95.054, 442.722, 92.136, -180, 0, -0.4] #旋轉商品
    arm_move('LIN',2000,100)


    # Point_Dist = [90.054, 527.898, 92.136, -180, 0, 90] #放入商品
    # arm_move('LIN',2000,100)

    modbus.DO(300,0)
    modbus.DO(303,0)

    Point_Dist = [90.054, 442.722, 257.898, -180, 0, 90] #原地抬高
    arm_move('LIN',2000,100)

    # Point_Dist = [90.054, 527.898, 249.173 ,-180, 0, 90] #原地抬高
    # arm_move('PTP',speed_setting,acceleration_setting)


    #商品1(鐵鋁罐)
    Point_Dist = [-15.310, 355.582, 247.439 ,-180, 0, 90] #到商品上方
    arm_move('PTP',speed_setting,acceleration_setting)
    
    Point_Dist = [-15.310, 355.582, 102.471 ,-180, 0, 90] #吸取位置
    arm_move('PTP',speed_setting,acceleration_setting)
    
    modbus.DO(300,1)
    modbus.DO(303,1)
    
    Point_Dist = [-15.310, 355.582, 342.487 ,-180, 0, 90] #原地抬高
    arm_move('PTP',speed_setting,acceleration_setting)
    
    Point_Dist = [84.050, 510.283, 342.487 ,-180, 0, 90] #到袋口
    arm_move('PTP',speed_setting,acceleration_setting)
    
    Point_Dist = [84.050, 510.283, 100.960 ,-180, 0, 90] #放入商品
    arm_move('LIN',2000,100)
    
    modbus.DO(300,0)
    modbus.DO(303,0)
    
    Point_Dist = [84.050, 510.283, 249.173 ,-180, 0, 90] #原地抬高
    arm_move('PTP',speed_setting,acceleration_setting)


    # Point_Dist = [90.054, 527.898, 200.073, -180, 0, -0.4] #旋轉商品
    # arm_move('PTP',speed_setting,acceleration_setting)

    # Point_Dist = [90.054, 442.722, 200.073, -180, 0, -0.4] #旋轉商品
    # arm_move('LIN',2000,100)

    # Point_Dist = [90.054, 442.722, 92.136, -180, 0, -0.4] #旋轉商品
    # arm_move('LIN',2000,100)


    # Point_Dist = [90.054, 442.722, 257.898, -180, 0, 90] #原地抬高
    # arm_move('LIN',2000,100)

#商品2-2(麥香2)
    # Point_Dist = [-200.931, 338.748, 257.062, -180, 0, 90] #到商品上方
    # arm_move('PTP',speed_setting,acceleration_setting)

    # Point_Dist = [-200.931, 338.748, 78.887, -180, 0, 90] #吸取商品
    # arm_move('PTP',speed_setting,acceleration_setting)

    # modbus.DO(300,1)
    # modbus.DO(303,1)    

    # Point_Dist = [-204.931, 338.748, 315.831, -180, 0, 90] #原地抬起
    # arm_move('PTP',speed_setting,acceleration_setting)

    # Point_Dist = [97.667, 504.132, 315.831, -180, 0, 90] #到袋口
    # arm_move('PTP',speed_setting,acceleration_setting)

    # Point_Dist = [97.667, 504.132, 200.073, -180, 0, 90] #放入商品
    # arm_move('LIN',2000,100)

    # Point_Dist = [97.667, 504.132, 200.073, -180, 0, -0.4] #旋轉商品
    # arm_move('LIN',2000,100)

    # Point_Dist = [97.667, 577.180, 200.073, -180, 0, -0.4] #往Y+前進
    # arm_move('LIN',2000,100)

    # Point_Dist = [97.667, 577.180, 92.136, -180, 0, -0.4] #放下物品
    # arm_move('LIN',2000,100)

    # modbus.DO(300,0)
    # modbus.DO(303,0)

    # Point_Dist = [97.667, 534.653, 255.016, -180, 0, -0.4] #原地抬高
    # arm_move('PTP',speed_setting,acceleration_setting)

#移動紙袋至出貨區
    Point_Dist = [240.713, 530.779, 255.016, -180, 0, -86.086] #至移動位置上方、旋轉RZ
    arm_move('PTP',speed_setting,acceleration_setting)

    #轉伺服馬達
    mm.motor_move(my_dxl,191) 

    Point_Dist = [240.713, 528.779, -14.824 ,-180, 0, -79.147] #到移動吸取位置
    arm_move('LIN',2000,100)   

    modbus.DO(300,1)
    modbus.DO(303,1)


    Point_Dist = [-161.327, 528.779, -14.824 ,-180, 0, -79.147] #移到出貨區
    arm_move('LIN',2000,100)

    modbus.DO(300,0)
    modbus.DO(303,0)

    #完成訂單1
    Point_Dist = [0, 523.445, 4.093 ,-180, 0, 3] #移到出貨區
    arm_move('PTP',speed_setting,acceleration_setting)
    # Point_Dist = [0, 523.445, 4.093 ,-180, 0, 3] #prepare going home
    arm_move('PTP',speed_setting,acceleration_setting)
    Point_Dist = Point_home
    PTP_Move(Point_Dist, speed_setting ,acceleration_setting)
    # 伺服馬達
    mm.motor_move(my_dxl,505)
    
    """

        訂單2

    """
    #拿取紙袋-工作區
    Point_Dist = [283.899, 258.249, 150 ,-180, 0, 90] #到紙袋吸取位置
    arm_move('PTP',speed_setting,acceleration_setting)
    
    Point_Dist = [283.899, 258.249, 38.877 ,-180, 0, 90] #到紙袋吸取位置
    arm_move('LIN',2000,100)
    
    modbus.DO(300,1)
    modbus.DO(303,1)
    
    Point_Dist = [355.673, 258.249, 261.957 ,-180, 0, 90] #抽出紙袋
    arm_move('PTP',speed_setting,acceleration_setting)
    
    Point_Dist = [82.674, 532.223, 261.957 ,-180, 0, 90] #前往卡扣區
    arm_move('PTP',speed_setting,acceleration_setting)
    
    Point_Dist = [82.674, 532.223, 72.095 ,-180, 0, 90] #貼地面
    arm_move('LIN',2000,100)
    
    Point_Dist = [254.223, 532.223, 72.095 ,-180, 0, 90] #進卡扣
    arm_move('LIN',2000,100)
    
    Point_Dist = [254.223, 532.223, 235.287 ,-180, 0, 90] #打開紙袋
    arm_move('LIN',2000,100)
    
    Point_Dist = [-2.528, 532.223, 235.287 ,-180, 0, 90] #離開打扣
    arm_move('LIN',2000,100)
    
    Point_Dist = [-2.528, 532.223, 286.489 ,-180, 0, 90] #原地抬高
    arm_move('PTP',speed_setting,acceleration_setting)
    
    #轉伺服馬達
    mm.motor_move(my_dxl,191)
    
    Point_Dist = [-2.528, 532.223, 156.990 ,-180, 0, 90] #貼齊地面
    arm_move('PTP',speed_setting,acceleration_setting)
    
    modbus.DO(300,0)
    modbus.DO(303,0)
    
    Point_Dist = [-2.528, 532.223, 247.439 ,-180, 0, 90] #原地抬高
    arm_move('PTP',speed_setting,acceleration_setting)
    
    #轉伺服馬達
    mm.motor_move(my_dxl,505)

    #商品2-2(麥香2)
    Point_Dist = [-200.931, 338.748, 257.062, -180, 0, 90] #到商品上方
    arm_move('PTP',speed_setting,acceleration_setting)

    Point_Dist = [-200.931, 338.748, 78.887, -180, 0, 90] #吸取商品
    arm_move('PTP',speed_setting,acceleration_setting)

    modbus.DO(300,1)
    modbus.DO(303,1)    

    Point_Dist = [-204.931, 338.748, 315.831, -180, 0, 90] #原地抬起
    arm_move('PTP',speed_setting,acceleration_setting)

    Point_Dist = [99.667, 518.211, 315.831, -180, 0, 90] #到袋口
    arm_move('PTP',speed_setting,acceleration_setting)

    Point_Dist = [99.667, 518.211, 92.136, -180, 0, 90] #放入商品
    arm_move('LIN',2000,100)

    # Point_Dist = [97.667, 504.132, 200.073, -180, 0, -0.4] #旋轉商品
    # arm_move('LIN',2000,100)

    # Point_Dist = [97.667, 577.180, 200.073, -180, 0, -0.4] #往Y+前進
    # arm_move('LIN',2000,100)

    # Point_Dist = [97.667, 577.180, 92.136, -180, 0, -0.4] #放下物品
    # arm_move('LIN',2000,100)

    modbus.DO(300,0)
    modbus.DO(303,0)

    Point_Dist = [99.667, 518.211, 255.016, -180, 0, 90] #原地抬高
    arm_move('PTP',speed_setting,acceleration_setting)
    
    # #商品1(鐵鋁罐)
    # Point_Dist = [-18.310, 355.582, 247.439 ,-180, 0, 90] #到商品上方
    # arm_move('PTP',speed_setting,acceleration_setting)
    
    # Point_Dist = [-18.310, 355.582, 102.471 ,-180, 0, 90] #吸取位置
    # arm_move('PTP',speed_setting,acceleration_setting)
    
    # modbus.DO(300,1)
    # modbus.DO(303,1)
    
    # Point_Dist = [-18.310, 355.582, 342.487 ,-180, 0, 90] #原地抬高
    # arm_move('PTP',speed_setting,acceleration_setting)
    
    # Point_Dist = [84.050, 516.283, 342.487 ,-180, 0, 90] #到袋口
    # arm_move('PTP',speed_setting,acceleration_setting)
    
    # Point_Dist = [84.050, 516.283, 105.960 ,-180, 0, 90] #放入商品
    # arm_move('LIN',2000,100)
    
    # modbus.DO(300,0)
    # modbus.DO(303,0)
    
    # Point_Dist = [84.050, 516.283, 249.173 ,-180, 0, 90] #原地抬高
    # arm_move('PTP',speed_setting,acceleration_setting)
    
    #商品2-1(奇趣蛋)
    Point_Dist = [110.455, 293.853, 249.173 ,-180, 0, 90] #到商品上方
    arm_move('PTP',speed_setting,acceleration_setting)
    
    Point_Dist = [110.455, 293.853, 153.368 ,-180, 0, 90] #吸取位置
    arm_move('PTP',speed_setting,acceleration_setting)
    
    modbus.DO(300,1)
    modbus.DO(303,1)
    
    Point_Dist = [110.455, 293.853, 297.918 ,-180, 0, 90] #原地抬高
    arm_move('PTP',speed_setting,acceleration_setting)
    
    Point_Dist = [90.480, 519.802, 297.918 ,-180, 0, 90] #到袋口
    arm_move('PTP',speed_setting,acceleration_setting)
    
    Point_Dist = [90.480, 519.802, 208.052 ,-180, 0, 90] #放入商品
    arm_move('LIN',2000,100)
    
    modbus.DO(300,0)
    modbus.DO(303,0)
    
    Point_Dist = [90.480, 519.802, 250.216 ,-180, 0, 90] #原地抬高
    arm_move('PTP',speed_setting,acceleration_setting)
    
    #商品2-2(奇趣蛋)
    Point_Dist = [110.055, 346.808, 250.216 ,-180, 0, 90] #到商品上方
    arm_move('PTP',speed_setting,acceleration_setting)
    
    Point_Dist = [110.055, 346.808, 153.116 ,-180, 0, 90] #到吸取位置
    arm_move('PTP',speed_setting,acceleration_setting)
    
    modbus.DO(300,1)
    modbus.DO(303,1)
    
    Point_Dist = [110.055, 346.808, 303.991 ,-180, 0, 90] #原地抬起
    arm_move('PTP',speed_setting,acceleration_setting)
    
    Point_Dist = [90.031, 515.283, 303.991 ,-180, 0, 90] #到袋口
    arm_move('PTP',speed_setting,acceleration_setting)
    
    Point_Dist = [90.031, 515.283, 187.591 ,-180, 0, 90] #放入商品
    arm_move('LIN',2000,100)
    
    modbus.DO(300,0)
    modbus.DO(303,0)
    
    Point_Dist = [90.031, 515.283, 253.691 ,-180, 0, 90] #原地抬起
    arm_move('PTP',speed_setting,acceleration_setting)
    
    #移動袋子
    Point_Dist = [252.620, 525.749, 253.691 ,-180, 0, -79.417] #到位置上方
    arm_move('PTP',speed_setting,acceleration_setting)
    
    #轉伺服馬達
    mm.motor_move(my_dxl,191)
    
    Point_Dist = [252.620, 525.49, -24.178 ,-180, 0, -79.417] #到吸取位置
    arm_move('LIN',2000,100)

    modbus.DO(300,1)
    modbus.DO(303,1)
    
    Point_Dist = [-56.830, 525.749, -24.178 ,-180, 0, -79.417] #到出貨區
    arm_move('LIN',2000,100)
    
    modbus.DO(300,0)
    modbus.DO(303,0)
    
    Point_Dist = [0, 516.283, -6.858 ,-180, 0, 3] #離開紙袋
    arm_move('PTP',speed_setting,acceleration_setting)
    
    # Point_Dist = [0, 536.583, -6.858 ,-180, 0, 3] #離開紙袋
    # arm_move('PTP',speed_setting,acceleration_setting)

    #結束任務
    Point_Dist = Point_home
    PTP_Move(Point_Dist, speed_setting ,acceleration_setting)

    #轉伺服馬達
    mm.motor_move(my_dxl,505)
    
    
    
cv2.destroyAllWindows()
