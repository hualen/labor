Point_Dist = [ 0  , 0.0, 0.0, -180.000, 0.0, 90.000]
speed_setting = 100
acceleration_setting = 20


def arm_move(mode, speed ,acceleration):
    if mode=='PTP':
        PTP_Move(Point_Dist, speed ,acceleration)  
    else:
        PTP_Move(Point_Dist, speed ,acceleration)

def PTP_Move(Point, speed ,acceleration):
    print("Start PTP Move!")
    print("Point = ",Point)
    print("Speed = ",speed)
    print("Acceleration = ",acceleration)

def LIN_Move(Point, speed ,acceleration):
    print("Start LIN Move!")
    print("Point = ",Point)
    print("Speed = ",speed)
    print("Acceleration = ",acceleration)

if __name__ == "__main__":
    arm_move("PTP",speed_setting,acceleration_setting)
    Point_Dist = [ 123, 456, 789, -180.000, 0.0, 90.000]
    arm_move("LIN",speed_setting,acceleration_setting)