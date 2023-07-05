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
sys.path.append("/home/hualen/ax12_control")
import order
from Ax12 import Ax12
import ax12move as mm


so_file = "/home/hualen/Desktop/bagging/Hiwin_API.so"
modbus = CDLL(so_file)

Point_home = [ 0  , 368.000, 293.500, -180.000, 0.000, 90.000]
Point_Dist = [ 0  , 0.0, 0.0, -180.000, 0.0, 90.000]
Angel_Dist = [ 0  ,  0, -0, 0, 9, -0]
Angel_home = [ 0  ,  -0, -0, -0, -90, -0]

put_tea = [

          ]


# """
#     motor setting
# """
# # e.g 'COM3' windows or '/dev/ttyUSB0' for Linux
# Ax12.DEVICENAME = '/dev/ttyUSB0'

# Ax12.BAUDRATE = 1_000_000
# Ax12.DEBUG = True
# # sets baudrate and opens com port
# Ax12.connect()

# # create AX12 instance with ID 10 
# motor_id = 1
# my_dxl = Ax12(motor_id)  
# my_dxl.set_moving_speed(1000)
# my_dxl.print_status

# # 手臂移動速度
# speed_setting = 50
# acceleration_setting = 20




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
    modbus.LIN(1, speed, acceleration, 1, 0, C_LIN_XYZ)
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
    modbus.PTP(0, speed, acceleration, 1, 0, C_PTP_XYZ)
    modbus.Arm_State_REGISTERS()
    while 1:
        modbus.PTP(0, speed, acceleration, 1, 0, C_PTP_XYZ)
        print('======================================')
        print('modbus= ',modbus.Arm_State_REGISTERS())
        print('======================================')
        if(modbus.Arm_State_REGISTERS() == 1):
            break
    # if(modbus.Arm_State_REGISTERS() == 1):
    #     modbus.R200()
            
    print("END Angel Move!" )



""""
主程式
    程式流程:
    1. 檢測影像
    2. 在原圖繪製結果
    3. 輸出影像
"""




if __name__ == "__main__":

    # '''
    #     手臂設定
    # '''
    # Arm_statePTP = 0
    # modbus.DO.argtypes = [c_int, c_int]
    # modbus.PTP.argtypes = [c_int, c_int, c_int, c_int, c_int]
    # modbus.LIN.argtypes = [c_int, c_int, c_int, c_int, c_int]
    # modbus.libModbus_Connect()
    # modbus.Holding_Registers_init()

    # # '''
    # #     吸嘴設定
    # # '''
    # IO_Port = 301 # D0
    # command = 200

    # modbus.DO(301,0) # 1 -> on ; 0 -> off
    # modbus.DO(303PTP_Angel,0) # 1 -> on ; 0 -> off
        
    # Point_Dist = Point_home
    # PTP_Move(Point_Dist, speed_setting ,acceleration_setting)

    #///////////////////////////////////////////////////////////
    order.start_order()
    forder = order.final_order
    print(forder)
    for index in range(0,4):
        print("執行第",index+1,"筆訂單")
        # Point_Dist = [282.312, 262.535, 296.660, -180, 0, 90] #到紙袋上方
        # arm_move('PTP',speed_setting,acceleration_setting)

        # Point_Dist = [282.312, 262.535, 57.075, -180, 0, 90] #到吸取袋高度
        # arm_move('PTP',speed_setting,acceleration_setting)

        # modbus.DO(300,1)
        # modbus.DO(303,1)

        # Point_Dist = [350.962, 262.535, 248.975, -180, 0, 90] #吸取紙袋
        # arm_move('PTP',speed_setting,acceleration_setting)

        # Point_Dist = [64.925, 533.154, 84.755, -180, 0, 90] #提高紙袋
        # arm_move('PTP',speed_setting,acceleration_setting)

        # Point_Dist = [260.375, 533.154, 84.755, -180, 0, 90] #離開紙袋區
        # arm_move('PTP',speed_setting,acceleration_setting)

        # Point_Dist = [260.375, 533.154, 197,290, -180, 0, 90] #到卡扣上
        # arm_move('PTP',speed_setting,acceleration_setting)

        # Point_Dist = [-4.475, 533.154, 197.290, -180, 0, 90] #離開卡扣
        # arm_move('PTP',speed_setting,acceleration_setting)

        # Point_Dist = [-4.475, 533.154, 268.085, -180, 0, 90] #工作區
        # arm_move('PTP',speed_setting,acceleration_setting)

        # mm.motor_move(my_dxl,90) #制具AX-12馬達移動

        # modbus.DO(300,0)
        # modbus.DO(303,0)
        
        # 麥香
        for num in range(0,forder[index][1]):
            print("現在吸取第",num+1,"個麥香")
            # 移動至取件座標
            # 吸取物品
            # 移到紙袋上方
            # 放下物品到一定高度
            # 移到袋內指定位置
            # 放開物品
            # 手臂抬起
            # 重複動作
        # 奇趣蛋
        for num in range(0,forder[index][0]):
            print("現在吸取第",num+1,"個奇趣蛋")
            # 移動至取件座標
            # 吸取物品
            # 移到紙袋上方
            # 放下物品到一定高度
            # 移到袋內指定位置
            # 放開物品
            # 手臂抬起
            # 重複動作
        # 泡芙
        for num in range(0,forder[index][2]):
            print("現在吸取第",num+1,"個泡芙")
            # 移動至取件座標
            # 吸取物品
            # 移到紙袋上方
            # 放下物品到一定高度
            # 移到袋內指定位置
            # 放開物品
            # 手臂抬起
            # 重複動作
        print("\n")
            
 

