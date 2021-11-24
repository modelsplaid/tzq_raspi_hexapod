# This module contains how to convert from joint angle to servo pulse


# leg number: 
#
#         x2          x1
#          \    *    /
#           *---*---*
#          /    |    \
#         /     |     \
#        /      |      \
#  x3 --*------cog------*-- x0
#        \      |      /
#         \     |     /
#          \    |    /
#           *---*---*
#          /         \
#         x4         x5
#

# -------------
# LINKAGE
# -------------
# Neutral position of the linkages (alpha=0, beta=0, gamma=0)
# note that at neutral position:
#  link b and link c are perpendicular to each other
#  link a and link b form a straight line
#  link a and the leg x axis are aligned
#
# alpha - the angle linkage a makes with x_axis about z axis
# beta - the angle that linkage a makes with linkage b
# gamma - the angle that linkage c make with the line perpendicular to linkage b
#
#
# MEASUREMENTS
#
#  |--- a--------|--b--|
#  |=============|=====| p2 -------
#  p0            p1    |          |
#                      |          |
#                      |          c
#                      |          |
#                      |          |
#                      | p3  ------
#
# p0 - body contact
# p1 - coxia point
# p2 - femur point
# p3 - foot tip
#
#  z axis
#  |
#  |
#  |------- x axis
# origin
#
#
# ANGLES beta and gamma
#                /
#               / beta
#         ---- /* ---------
#        /    //\\        \
#       b    //  \\        \
#      /    //    \\        c
#     /    //beta  \\        \
# *=======* ---->   \\        \
# |---a---|          \\        \
#                     *-----------
#
# |--a--|---b----|
# *=====*=========* -------------
#               | \\            \
#               |  \\            \
#               |   \\            c
#               |    \\            \
#               |gamma\\            \
#               |      *----------------
#



# Joint direction definition: 
# For joint beta and gamma: positive: move up. negative: move dowm
# For right side alpha: positive: move forward. negative: move backward.
# For left side alpha : positive: move backward. negative: move forward.
import time
import sys
sys.path.append("../")
from HiwonderSDK import Board

class VirtualToReal:
    
    #Number of pulses needed to rotate one degree 
    pulses_per_deg = 395.0/90.0

    #Number of degrees needed to rotate one pulse
    degs_per_pulse = 1.0/pulses_per_deg
    
    # Pulses for each servo when alpha beta and gamma all equal to zero
    nutural_poses_pulse = {
    0: {"coxia": 493, "femur": 500, "tibia": 690, "name": "right-middle", "id": 0},
    1: {"coxia": 317, "femur": 460, "tibia": 685, "name": "right-front", "id": 1},
    2: {"coxia": 704, "femur": 500, "tibia": 319, "name": "left-front", "id": 2},
    3: {"coxia": 493, "femur": 500, "tibia": 288, "name": "left-middle", "id": 3},
    4: {"coxia": 310, "femur": 500, "tibia": 322, "name": "left-back", "id": 4},
    5: {"coxia": 690, "femur": 520, "tibia": 708, "name": "right-back", "id": 5},
    }

    nutural_poses_deg = {
    0: {"coxia": 0, "femur": 0, "tibia": 0, "name": "right-middle", "id": 0},
    1: {"coxia": 0, "femur": 0, "tibia": 0, "name": "right-front", "id": 1},
    2: {"coxia": 0, "femur": 0, "tibia": 0, "name": "left-front", "id": 2},
    3: {"coxia": 0, "femur": 0, "tibia": 0, "name": "left-middle", "id": 3},
    4: {"coxia": 0, "femur": 0, "tibia": 0, "name": "left-back", "id": 4},
    5: {"coxia": 0, "femur": 0, "tibia": 0, "name": "right-back", "id": 5},
    }

    # If servo rotation direction same as model joint angle, set 1
    # if opposite set -1.   
    # todo: here
    direction_poses_pulse = {
    0: {"coxia": 1, "femur": 1, "tibia": -1, "name": "right-middle", "id": 0},
    1: {"coxia": 1, "femur": 1, "tibia": -1, "name": "right-front", "id": 1},
    2: {"coxia": -1, "femur": -1, "tibia": 1, "name": "left-front", "id": 2},
    3: {"coxia": -1, "femur": -1, "tibia": 1, "name": "left-middle", "id": 3},
    4: {"coxia": -1, "femur": -1, "tibia": 1, "name": "left-back", "id": 4},
    5: {"coxia": 1, "femur": 1, "tibia": -1, "name": "right-back", "id": 5},
    }

    # joint of our hexa model has different  ids with the real-world servo 
    # each entry stands for corresponding servo id
    servo_id_mapping = {
    0: {"coxia": 13, "femur": 14, "tibia": 15, "name": "right-middle", "id": 0},
    1: {"coxia": 16, "femur": 17, "tibia": 18, "name": "right-front", "id": 1},
    2: {"coxia": 7, "femur": 8, "tibia": 9, "name": "left-front", "id": 2},
    3: {"coxia": 4, "femur": 5, "tibia": 6, "name": "left-middle", "id": 3},
    4: {"coxia": 1, "femur": 2, "tibia": 3, "name": "left-back", "id": 4},
    5: {"coxia": 10, "femur": 11, "tibia": 12, "name": "right-back", "id": 5},
    }
  
     # the pulses will send to servo
    pulses2servos = {
    0: {"coxia": 0, "femur": 0, "tibia": 0, "name": "right-middle", "id": 0},
    1: {"coxia": 0, "femur": 0, "tibia": 0, "name": "right-front", "id": 1},
    2: {"coxia": 0, "femur": 0, "tibia": 0, "name": "left-front", "id": 2},
    3: {"coxia": 0, "femur": 0, "tibia": 0, "name": "left-middle", "id": 3},
    4: {"coxia": 0, "femur": 0, "tibia": 0, "name": "left-back", "id": 4},
    5: {"coxia": 0, "femur": 0, "tibia": 0, "name": "right-back", "id": 5},
    }

    # given joint angle of hexapod, get servo pulse for each joint
    def join_pose2pulse(self,poses):
        #1. Loop over each joint angle        
        #2. Find which joint id maps to which servo id         
        #3. Decide pulse number based on direction mapping, 
        #   Num pulses per deg  
        for i in range(len(poses)): 
            pose = poses[i]
            
            # get input angles   
            print("Joint angles for pose id: "+str(poses[i]["id"])+ \
                                " coxia: "+ str(pose["coxia"])+ \
                                " femur: "+ str( pose["femur"])+ \
                                " tibia: " + str( pose["tibia"]))                        

            ### convert joint angle to sevo pulse 
            # compute coxia pulse
            self.pulses2servos[i]["coxia"] = self.nutural_poses_pulse[i]["coxia"] + \
                self.direction_poses_pulse[i]["coxia"] * self.pulses_per_deg * pose["coxia"]              

            # compute femur pulse 
            self.pulses2servos[i]["femur"] = self.nutural_poses_pulse[i]["femur"] + \
                self.direction_poses_pulse[i]["femur"] * self.pulses_per_deg * pose["femur"]               

            # compute tibia pulse 
            self.pulses2servos[i]["tibia"] = self.nutural_poses_pulse[i]["tibia"] + \
                self.direction_poses_pulse[i]["tibia"] * self.pulses_per_deg * pose["tibia"]     

        return self.pulses2servos

    # send servo pulse to real bot
    def SendBusServoPulse(self,time_msec,pulses2Servos):
        
        for i in range(len(pulses2Servos)): 

            leg_pose = pulses2Servos[i]
            leg_servos = self.servo_id_mapping[i]

            coxia_pulse = leg_pose["coxia"]
            coxia_servo_id = leg_servos["coxia"]
            Board.setBusServoPulse(coxia_servo_id, coxia_pulse, time_msec)

            femur_pulse = leg_pose["femur"]
            femur_servo_id = leg_servos["femur"]
            Board.setBusServoPulse(femur_pulse, femur_servo_id, time_msec)

            tibia_pulse = leg_pose["femur"]
            tibia_servo_id = leg_servos["femur"]
            Board.setBusServoPulse(tibia_pulse, tibia_servo_id, time_msec)

if __name__ == "__main__": 
    v2r = VirtualToReal()     
    time.sleep(0.5)
    pulses2servos = v2r.join_pose2pulse(v2r.nutural_poses_deg)
    v2r.SendBusServoPulse(1000,pulses2servos)