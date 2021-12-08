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
from copy import deepcopy
sys.path.append("../")
from . import const_hardware
from HiwonderSDK import Board
from copy import deepcopy

class VirtualToReal:
    
    #Number of pulses needed to rotate one degree 
    pulses_per_deg = 395.0/90.0

    #Number of degrees needed to rotate one pulse
    degs_per_pulse = 1.0/pulses_per_deg
    
    # Pulses for each servo when alpha beta and gamma all equal to zero
    nutural_poses_pulse = deepcopy(const_hardware.NUTURAL_POSES_PULSE)

    nutural_poses_deg  = deepcopy(const_hardware.NUTURAL_POSES_DEG)

    # If servo rotation direction same as model joint angle, set 1
    # if opposite set -1.   
    # todo: here
    direction_poses_pulse = deepcopy(const_hardware.DIRECTION_POSES_PULSE)

    # joint of our hexa model has different  ids with the real-world servo 
    # each entry stands for corresponding servo id
    #
    servo_id_mapping = deepcopy(const_hardware.SERVO_ID_MAPPING)
  
     # the pulses will send to servo   
    pulses2servos = deepcopy(const_hardware.PULSES2SERVOS)

    def update_puses(self,poses_json_dict): 
        poses = deepcopy(self.nutural_poses_deg)

        for pose in poses_json_dict.values():
            i = pose["id"]
            poses[i]["coxia"] = pose["coxia"]
            poses[i]["femur"] = pose["femur"]
            poses[i]["tibia"] = pose["tibia"]

        pulses2servos = self.join_pose2pulse(poses)
        return pulses2servos

    # given joint angle of hexapod, get servo pulse for each joint
    def join_pose2pulse(self,poses):
        #1. Loop over each joint angle        
        #2. Find which joint id maps to which servo id         
        #3. Decide pulse number based on direction mapping, 
        #   Num pulses per deg  
        print("length of poses: "+ str(len(poses)))
        print(poses[0])
        for i in range(len(poses)): 
            pose = poses[i]
            print("poses number: " + str(i))
            print(pose)
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
            
            leg_pose =   pulses2Servos[i]
            leg_servos = self.servo_id_mapping[i]

            coxia_pulse = int(leg_pose["coxia"])
            coxia_servo_id = int(leg_servos["coxia"])
            Board.setBusServoPulse(coxia_servo_id, coxia_pulse, time_msec)            

            femur_pulse = int(leg_pose["femur"])
            femur_servo_id = int(leg_servos["femur"])
            Board.setBusServoPulse( femur_servo_id,femur_pulse, time_msec)            

            tibia_pulse = int(leg_pose["tibia"])
            tibia_servo_id = int(leg_servos["tibia"])
            Board.setBusServoPulse(tibia_servo_id,tibia_pulse,  time_msec)


def TestForwardKinematics():
    v2r = VirtualToReal()     
    time.sleep(0.5)
    pulses2servos = v2r.join_pose2pulse(v2r.nutural_poses_deg)
    v2r.SendBusServoPulse(1000,pulses2servos)
    time.sleep(1)

    coxia_poses_deg = {
    0: {"coxia": 30, "femur": 0, "tibia": 0, "name": "right-middle", "id": 0},
    1: {"coxia": 30, "femur": 0, "tibia": 0, "name": "right-front", "id": 1},
    2: {"coxia": 30, "femur": 0, "tibia": 0, "name": "left-front", "id": 2},
    3: {"coxia": 30, "femur": 0, "tibia": 0, "name": "left-middle", "id": 3},
    4: {"coxia": 30, "femur": 0, "tibia": 0, "name": "left-back", "id": 4},
    5: {"coxia": 30, "femur": 0, "tibia": 0, "name": "right-back", "id": 5},
    }

    pulses2servos = v2r.join_pose2pulse(coxia_poses_deg)
    v2r.SendBusServoPulse(1000,pulses2servos)
    time.sleep(1)

    coxia_femur_poses_deg = {
    0: {"coxia": 30, "femur": 30, "tibia": 0, "name": "right-middle", "id": 0},
    1: {"coxia": 30, "femur": 30, "tibia": 0, "name": "right-front", "id": 1},
    2: {"coxia": 30, "femur": 30, "tibia": 0, "name": "left-front", "id": 2},
    3: {"coxia": 30, "femur": 30, "tibia": 0, "name": "left-middle", "id": 3},
    4: {"coxia": 30, "femur": 30, "tibia": 0, "name": "left-back", "id": 4},
    5: {"coxia": 30, "femur": 30, "tibia": 0, "name": "right-back", "id": 5},
    }
    pulses2servos = v2r.join_pose2pulse(coxia_femur_poses_deg)
    v2r.SendBusServoPulse(1000,pulses2servos)
    time.sleep(1)

    coxia_femur_tibia_poses_deg = {
    0: {"coxia": 30, "femur": 30, "tibia": 30, "name": "right-middle", "id": 0},
    1: {"coxia": 30, "femur": 30, "tibia": 30, "name": "right-front", "id": 1},
    2: {"coxia": 30, "femur": 30, "tibia": 30, "name": "left-front", "id": 2},
    3: {"coxia": 30, "femur": 30, "tibia": 30, "name": "left-middle", "id": 3},
    4: {"coxia": 30, "femur": 30, "tibia": 30, "name": "left-back", "id": 4},
    5: {"coxia": 30, "femur": 30, "tibia": 30, "name": "right-back", "id": 5},
    }
    pulses2servos = v2r.join_pose2pulse(coxia_femur_tibia_poses_deg)
    v2r.SendBusServoPulse(1000,pulses2servos)    
    time.sleep(1)
    # reset 
    pulses2servos = v2r.join_pose2pulse(v2r.nutural_poses_deg)
    v2r.SendBusServoPulse(1000,pulses2servos)

if __name__ == "__main__": 

    TestForwardKinematics()