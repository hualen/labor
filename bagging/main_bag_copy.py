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
# import YOLO_Detect



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

"""
    realsense setting
"""
# pipeline = rs.pipeline()
# config = rs.config()
# config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
# config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
# pipeline.start(config)
# sensor = pipeline.get_active_profile().get_device().query_sensors()[1]
# sensor.set_option(rs.option.auto_exposure_priority, True)


"""
    motor setting
"""
# e.g 'COM3' windows or '/dev/ttyUSB0' for Linux
Ax12.DEVICENAME = '/dev/ttyUSB0'

Ax12.BAUDRATE = 1_000_000
Ax12.DEBUG = True
# sets baudrate and opens com port
Ax12.connect()

# create AX12 instance with ID 10 
motor_id = 1
my_dxl = Ax12(motor_id)  
my_dxl.set_moving_speed(1000)
my_dxl.print_status

# 手臂移動速度
speed_setting = 50
acceleration_setting = 20




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
影像檢測
    輸入:(影像位置,神經網路,物件名稱集,信心值閥值(0.0~1.0))
    輸出:(檢測後影像,檢測結果)
    註記:
"""
def image_detection(image, network, class_names, class_colors, thresh):
    width = darknet.network_width(network)
    height = darknet.network_height(network)
    darknet_image = darknet.make_image(width, height, 3)

    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_resized = cv2.resize(image_rgb, (width, height),
                               interpolation=cv2.INTER_LINEAR)

    darknet.copy_image_from_bytes(darknet_image, image_resized.tobytes())
    detections = darknet.detect_image(network, class_names, darknet_image, thresh=thresh)
    darknet.free_image(darknet_image)
    image = darknet.draw_boxes(detections, image_resized, class_colors)


    return detections



"""
座標轉換
    輸入:(YOLO座標,原圖寬度,原圖高度)
    輸出:(框的左上座標,框的右下座標)
    註記:
"""
def bbox2points(bbox,W,H):
    """
    From bounding box yolo format
    to corner points cv2 rectangle
    """ 
    width = darknet.network_width(network)      # YOLO壓縮圖片大小(寬)
    height = darknet.network_height(network)    # YOLO壓縮圖片大小(高)

    x, y, w, h = bbox                           # (座標中心x,座標中心y,寬度比值,高度比值)
    x = x*W/width
    y = y*H/height
    w = w*W/width
    h = h*H/height
    x1 = int(round(x - (w / 2)))
    x2 = int(round(x + (w / 2)))
    y1 = int(round(y - (h / 2)))
    y2 = int(round(y + (h / 2)))
    
    return x1, y1, x2, y2


"""
原圖繪製檢測框線
    輸入:(檢測結果,原圖位置,框線顏色集)
    輸出:(影像結果)
    註記:
"""
def boxes(detections, image, colors):
    H,W,_ = image.shape
    img = image.copy()

    for label, confidence, bbox in detections:
        x1, y1, x2, y2 = bbox2points(bbox,W,H)

        cv2.rectangle(img, (x1, y1), (x2, y2), colors[label], 1)
        cv2.putText(img, "{} [{:.2f}]".format(label, float(confidence)),
                    (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    colors[label], 2)
        # 輸出框座標_加工格式座標(左上點座標,右上點座標)
        print("\t{}\t: {:3.2f}%    (x1: {:4.0f}   y1: {:4.0f}   x2: {:4.0f}   y2: {:4.0f})".format(label, float(confidence), x1, y1, x2, y2))


    return img, x1, y1, x2, y2



"""Point_Dist= Angel_Dist
    PTP_Angel(Point_Dist,speed_setting,acceleration_setting)
主程式
    程式流程:
    1. 檢測影像
    2. 在原圖繪製結果
    3. 輸出影像
"""




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
        
    # Point_Dist = Point_home
    # PTP_Move(Point_Dist, speed_setting ,acceleration_setting)

    #///////////////////////////////////////////////////////////
    Point_Dist = Point_home
    PTP_Move(Point_Dist, speed_setting ,acceleration_setting)

    Point_Dist = [282.312, 262.535, 296.660, -180, 0, 90] #到紙袋上方
    arm_move('PTP',speed_setting,acceleration_setting)

    Point_Dist = [282.312, 262.535, 57.075, -180, 0, 90] #到吸取袋高度
    arm_move('PTP',speed_setting,acceleration_setting)

    modbus.DO(300,1)
    modbus.DO(303,1)

    Point_Dist = [350.962, 262.535, 248.975, -180, 0, 90] #吸取紙袋
    arm_move('PTP',speed_setting,acceleration_setting)

    Point_Dist = [64.925, 533.154, 84.755, -180, 0, 90] #提高紙袋
    arm_move('PTP',speed_setting,acceleration_setting)

    Point_Dist = [260.375, 533.154, 84.755, -180, 0, 90] #離開紙袋區
    arm_move('PTP',speed_setting,acceleration_setting)

    Point_Dist = [260.375, 533.154, 197,290, -180, 0, 90] #到卡扣上
    arm_move('PTP',speed_setting,acceleration_setting)

    Point_Dist = [-4.475, 533.154, 197.290, -180, 0, 90] #離開卡扣
    arm_move('PTP',speed_setting,acceleration_setting)

    Point_Dist = [-4.475, 533.154, 268.085, -180, 0, 90] #工作區
    arm_move('PTP',speed_setting,acceleration_setting)

    mm.motor_move(my_dxl,90) #制具AX-12馬達移動

    modbus.DO(300,0)
    modbus.DO(303,0)
    #///////////////////////////////////////////////////////////
    
    # Point_Dist = [270.729, 236.689, 180, -180, 0, 90] #到紙袋上方
    # arm_move('PTP',speed_setting,acceleration_setting)
    # Point_Dist = [270.729, 236.689, 83.657, -180, 0, 90] #吸取紙袋
    # arm_move('PTP',speed_setting,acceleration_setting)

    # modbus.DO(300,1)
    # modbus.DO(303,1)

    # Point_Dist = [270.729, 236.689, 180, -180, 0, 90] #提起紙袋
    # arm_move('PTP',speed_setting,acceleration_setting)
   
    # Point_Dist = [145.69, 487.525, 150.34, -180, 0, 90] #對準卡扣
    # arm_move('PTP',speed_setting,acceleration_setting)

    # Point_Dist = [145.69, 487.525, 91.34, -180, 0, 90]  #對準卡扣
    # arm_move('PTP',speed_setting,acceleration_setting)

    # Point_Dist = [283.849, 487.525, 91.34, -180, 0, 90]  #插入卡扣
    # arm_move('PTP',50,30)

    # Point_Dist = [359.259, 505.525, 217.720, -180, 0, 90]  #拉開紙袋
    # arm_move('PTP',speed_setting,acceleration_setting)

    # Point_Dist = [300.259, 505.525, 217.720, -180, 0, 90]  #拉開紙袋
    # arm_move('PTP',speed_setting,acceleration_setting)

    # Point_Dist = [300.259, 505.525, 230.720, -180, 0, 90]  #拉開紙袋
    # arm_move('PTP',speed_setting,acceleration_setting)

    # Point_Dist = [68.73, 487.525, 221.991, -180, 0, 90]  #拉出紙袋
    # arm_move('PTP',speed_setting,acceleration_setting)

    # Point_Dist = [68.73, 487.525, 221.991, 121.687, 0.022, 90]  #旋轉紙袋
    # arm_move('PTP',speed_setting,acceleration_setting)

    # Point_Dist = [68.73, 487.525, 185.054, 121.687, 0.022, 90]  #放下一點
    # arm_move('PTP',speed_setting,acceleration_setting)

    # Point_Dist = [3.983, 487.525, 190.054, 148.235, 2.288, 90]  #旋轉紙袋
    # arm_move('PTP',speed_setting,acceleration_setting)

    # Point_Dist = [0, 487.525, 190.054, 148.235, 2.288, 90]  #旋轉紙袋
    # arm_move('PTP',speed_setting,acceleration_setting)

    # modbus.DO(300,0)
    # modbus.DO(303,0)
    
    # Point_Dist = Point_home
    # arm_move('PTP',speed_setting,acceleration_setting)
    
    
cv2.destroyAllWindows()
