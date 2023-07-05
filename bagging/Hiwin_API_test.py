from calendar import c
from operator import mod
import numpy as np
from ctypes import *
import time
import rospy
'''
    DO(int DO_Num, int x)                                                         # 1 -> on ; 0 -> off                                          
    HOME(int state)                                                               # 1 RUN
    PTP(int type, int vel, int acc, int TOOL, int BASE, double *Angle)            # 0 -> joint ; 1 -> coordinate
    LIN(int type,double *XYZ, int vel, int acc, int TOOL, int BASE)               # 0 -> joint ; 1 -> coordinate
    CIRC(double *CIRC_s, double *CIRC_end, int vel, int acc, int TOOL, int BASE) 
    JOG(int joint,int dir)
'''

so_file = "./Hiwin_API.so"
modbus = CDLL(so_file)

def trans (L,H):

    ans = 0
    ans = (H*65536+L)/1000
    return ans



if __name__ == "__main__":
    i=0
    arm_coordinates=[]
    angle=[]
    Arm_state = 0
    PTP_Angle = [0, 0, 0, 0, -90, 0]                 # ANGLE
    PTP_XYZ   = [204.049, 368, 293.5, 180, 0, 90]    # XYZABC
    home_XYZ   = [0, 368, 293.5, 180, 0, 90]    # XYZABC
    LIN_Angle = [0, 0, 0, 0, -90, 90]                # ANGLE
    LIN_XYZ   = [204.049, 368, 110, 180, 0, 90]      # XYZABC
    CIRC_centre = [0, 460.823, 293.5, 180, 0, 90]      # CIRC centre point
    CIRC_end  = [-204.049, 368, 293.5, 180, 0, 90]   # CIRC end point
    IO_Port = 301 # D0
    arm_add = [400,401,402,403,404,405,406,407,408,409,410,411]
     
    C_PTP_Angle = (c_double * len(PTP_Angle))(*PTP_Angle)       # C Array
    C_PTP_XYZ = (c_double * len(PTP_XYZ))(*PTP_XYZ)             # C Array
    C_home_XYZ = (c_double * len(home_XYZ))(*home_XYZ)             # C Array
    C_CIRC_centre = (c_double * len(CIRC_centre))(*CIRC_centre) # C Array
    C_CIRC_end = (c_double * len(CIRC_end))(*CIRC_end)          # C Array
    
    modbus.DO.argtypes = [c_int, c_int]
    modbus.PTP.argtypes = [c_int, c_int, c_int, c_int, c_int]
    modbus.CIRC.argtypes = [c_int, c_int, c_int, c_int]
    modbus.Read_REGISTERS.argtypes = [c_int]

    # while 1:
    modbus.libModbus_Connect()
    modbus.Holding_Registers_init()

    # modbus.PTP(0, 10, 10, 1, 0, C_PTP_Angle)
    # modbus.CIRC(10, 10, 1, 0, C_CIRC_centre, C_CIRC_end)

    # modbus.DO(IO_Port,0) # 1 -> on ; 0 -> off
    # while 1:
        # rospy.init_node('libmodbus_ROS')

        # modbus.Holding_Registers_init()
        # modbus.HOME() # 1 RUN
        # modbus.PTP(1, 100, 10, 1, 0, C_PTP_XYZ)
        # modbus.DO(IO_Port,0) # 1 -> on ; 0 -> off
    
    # if(modbus.Arm_State_REGISTERS() == 0):
    modbus.PTP(1, 100, 10, 1, 0, C_PTP_XYZ)

    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(modbus.Arm_State_REGISTERS())
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    # while(1):
    #     # if(modbus.Arm_State_REGISTERS() == 2):
    #     #     modbus.PTP(1, 100, 10, 1, 0, C_PTP_XYZ)
    #     #     print(modbus.Arm_State_REGISTERS())

    #     if(modbus.Arm_State_REGISTERS() == 1):  
    #         modbus.PTP(1, 100, 10, 1, 0, C_home_XYZ)
    #         print(modbus.Arm_State_REGISTERS())
    #     else:
    #         modbus.Modbus_Close()
    #         print("Modbus Close")
    #         break

    # 讀取直角座標 
    for i in range(12):
        arm_coordinates.append(modbus.Read_REGISTERS(arm_add[i]))
    
    X_angle = trans(arm_coordinates[0],arm_coordinates[1])
    Y_angle = trans(arm_coordinates[2],arm_coordinates[3])
    Z_angle = trans(arm_coordinates[4],arm_coordinates[5])
    A_angle = trans(arm_coordinates[6],arm_coordinates[7])
    B_angle = trans(arm_coordinates[8],arm_coordinates[9])
    C_angle = trans(arm_coordinates[10],arm_coordinates[11])
    print("=======================================================")
    print(arm_coordinates)
    print("X:",X_angle)
    print("Y:",Y_angle)
    print("Z:",Z_angle)
    print("A:",A_angle)
    print("B:",B_angle)
    print("C:",C_angle)
    print("=======================================================")