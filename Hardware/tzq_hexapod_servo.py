# An interface between hexapod simulator and hiwonder hexapod
import time

import sys
sys.path.append("../")

from HiwonderSDK import Board
Board.setBusServoPulse(1, 800, 1000)
time.sleep(1) 
for i in range(19):
    Board.unloadBusServo(i)
