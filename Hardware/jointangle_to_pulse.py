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
import os
import json
from copy import deepcopy
sys.path.append("../")
from . import const_hardware
#import const_hardware
from mini_socket.mini_socket_sdk.libclient import MiniSocketClient 
from copy import deepcopy


class ClientServoCommu:
    def __init__(self,socket_config_file_name='Hardware/net_commu_config.json'):
        self.m_sock_client = MiniSocketClient(socket_config_file_name)
        self.commu_template = []
        self.load_servo_commu_template()
    
    def load_servo_commu_template(self,servo_commu_template_file = "Hardware/servo_commu.json"):    
        print("loading servo communication template")
        with open(servo_commu_template_file, "r") as fObj:
            servo_commu_template = json.load(fObj)
        #print("self.servo_commu_template: " + str(servo_commu_template))
        strservo = json.dumps(servo_commu_template)
        print("len of str servo commu: "+str(len(strservo)) )
        self.commu_template = servo_commu_template
        return servo_commu_template

    def test_recv_servos(self):
        one_frame=self.m_sock_client.pop_receiver_queue()
        while one_frame is not False:
            one_frame=self.m_sock_client.pop_receiver_queue()
            print("---- received from server data: "+str(one_frame))
        time.sleep(0.01)

    def test_send_servos(self):
        servo_commu_template = self.load_servo_commu_template()
        send_data = deepcopy(servo_commu_template)
        while(True):
            for i in send_data: 
                send_data[i]['send_servo_valid'] = True
                send_data[i]['send_servo_pos_val'] = 2000
                send_data[i]['send_servo_speed_val'] = 1000
                send_data[i]['send_servo_torque_val'] = 500
            
            str_send_data = json.dumps(send_data)
            self.m_sock_client.push_sender_queu(str_send_data)        
            time.sleep(1)

            for i in send_data: 
                send_data[i]['send_servo_valid'] = True
                send_data[i]['send_servo_pos_val'] = 1000
                send_data[i]['send_servo_speed_val'] = 1000
                send_data[i]['send_servo_torque_val'] = 500
            
            str_send_data = json.dumps(send_data)
            self.m_sock_client.push_sender_queu(str_send_data)
            time.sleep(1)
            self.test_recv_servos()




class VirtualToReal:
    
    #Number of pulses needed to rotate one degree 
    pulses_per_deg = 4096.0/360.0

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

    def __init__(self):

        self.DEFAULT_PULSE_SPEED = 500
        self.DEFAULT_TORQUE_VALUE = 300
        self.VALID_MIN_PULSE_SPEED = 1
        self.VALID_MAX_PULSE_SPEED = 3000

        self.servo_commu = ClientServoCommu()
        time.sleep(0.1)
        print("Going to netural position")
        pulses2servos = self.join_pose2pulse(self.nutural_poses_deg)
        self.pre_servo_pulses = deepcopy(pulses2servos)
        self.SendBusServoPulse(1,pulses2servos)
        time.sleep(3)


    def compute_pulse_speed(self,pose_old,pose_new,run_time_sec):

        pose_diffs = abs(pose_new-pose_old) 
        if(pose_diffs < 0): 
            speed_new = self.DEFAULT_PULSE_SPEED
            print("!!!Invalid servo pose diffs, use default speed")
            return speed_new
        if(run_time_sec <= 0):
            speed_new = self.DEFAULT_PULSE_SPEED
            print("!!!Invalid servo speed, use default speed")
            return speed_new
        
        speed_new = (pose_diffs)/run_time_sec
        speed_new = int(speed_new)
        #todo: check speed valid    
        if((self.VALID_MIN_PULSE_SPEED > speed_new) or (self.VALID_MAX_PULSE_SPEED < speed_new)):
            #print("!!!Calculated speed out of valid range, use default speed")
            #print("speed_new:"+str(speed_new) )
            speed_new = self.DEFAULT_PULSE_SPEED
            return speed_new

        return speed_new

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
        #print("length of poses: "+ str(len(poses)))
        #print(poses[0])
        for i in range(len(poses)): 
            pose = poses[i]
            #print("poses number: " + str(i))
            #print(pose)
            # get input angles   
            #print("Joint angles for pose id: "+str(poses[i]["id"])+ \
            #                    " coxia: "+ str(pose["coxia"])+ \
            #                    " femur: "+ str( pose["femur"])+ \
            #                    " tibia: " + str( pose["tibia"]))                        

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
        net_commu_servo_send = deepcopy(self.servo_commu.commu_template) 
        #print("---net_commu_servo_send:"+str(net_commu_servo_send) )
        #here

        for i in range(len(pulses2Servos)): 
            
            leg_pose =   pulses2Servos[i]
            pre_leg_pose = self.pre_servo_pulses[i] 
            leg_servos = self.servo_id_mapping[i]

            coxia_pulse = int(leg_pose["coxia"])
            pre_coxia_pulse = int(pre_leg_pose["coxia"])
            coxia_servo_id = int(leg_servos["coxia"])
            net_commu_servo_index = "serial_servo_"+str(coxia_servo_id)
            net_commu_servo_send[net_commu_servo_index]['send_servo_valid'] = True
            net_commu_servo_send[net_commu_servo_index]['send_servo_pos_val'] = coxia_pulse
            pulse_speed = self.compute_pulse_speed(pre_coxia_pulse,coxia_pulse,time_msec/1000)
            net_commu_servo_send[net_commu_servo_index]['send_servo_speed_val'] = pulse_speed
            net_commu_servo_send[net_commu_servo_index]['send_servo_torque_val'] = self.DEFAULT_TORQUE_VALUE

            femur_pulse = int(leg_pose["femur"])
            pre_femur_pulse = int(pre_leg_pose["femur"])
            femur_servo_id = int(leg_servos["femur"])
            net_commu_servo_index = "serial_servo_"+str(femur_servo_id)
            net_commu_servo_send[net_commu_servo_index]['send_servo_valid'] = True
            net_commu_servo_send[net_commu_servo_index]['send_servo_pos_val'] = femur_pulse
            pulse_speed = self.compute_pulse_speed(pre_femur_pulse,femur_pulse,time_msec/1000)
            net_commu_servo_send[net_commu_servo_index]['send_servo_speed_val'] = pulse_speed
            net_commu_servo_send[net_commu_servo_index]['send_servo_torque_val'] = self.DEFAULT_TORQUE_VALUE

            tibia_pulse = int(leg_pose["tibia"])
            pre_tibia_pulse = int(pre_leg_pose["tibia"])
            tibia_servo_id = int(leg_servos["tibia"])
            #Board.setBusServoPulse(tibia_servo_id,tibia_pulse,  time_msec)
            net_commu_servo_index = "serial_servo_"+str(tibia_servo_id)
            net_commu_servo_send[net_commu_servo_index]['send_servo_valid'] = True
            net_commu_servo_send[net_commu_servo_index]['send_servo_pos_val'] = tibia_pulse
            pulse_speed = self.compute_pulse_speed(pre_tibia_pulse,tibia_pulse,time_msec/1000)
            net_commu_servo_send[net_commu_servo_index]['send_servo_speed_val'] = pulse_speed
            net_commu_servo_send[net_commu_servo_index]['send_servo_torque_val'] = self.DEFAULT_TORQUE_VALUE
            
        self.pre_servo_pulses = deepcopy(pulses2Servos)   

        str_send_data = json.dumps(net_commu_servo_send)
        self.servo_commu.m_sock_client.push_sender_queu(str_send_data)
def TestNutualPositions():
    v2r = VirtualToReal()     
    time.sleep(0.5)
    print("sending to servo")
    pulses2servos = v2r.join_pose2pulse(v2r.nutural_poses_deg)
    v2r.SendBusServoPulse(1000,pulses2servos)
    time.sleep(3)
    print("done sending to servo")

def TestForwardKinematics():
    v2r = VirtualToReal()     
    coxia_poses_deg = {
    0: {"coxia": 30, "femur": 0, "tibia": 0, "name": "right-middle", "id": 0},
    1: {"coxia": 30, "femur": 0, "tibia": 0, "name": "right-front", "id": 1},
    2: {"coxia": 30, "femur": 0, "tibia": 0, "name": "left-front", "id": 2},
    3: {"coxia": 30, "femur": 0, "tibia": 0, "name": "left-middle", "id": 3},
    4: {"coxia": 30, "femur": 0, "tibia": 0, "name": "left-back", "id": 4},
    5: {"coxia": 30, "femur": 0, "tibia": 0, "name": "right-back", "id": 5},
    }
    pulses2servos = v2r.join_pose2pulse(coxia_poses_deg)
    v2r.SendBusServoPulse(3000,pulses2servos)
    time.sleep(3)

    
    coxia_femur_poses_deg = {
    0: {"coxia": 30, "femur": 30, "tibia": 0, "name": "right-middle", "id": 0},
    1: {"coxia": 30, "femur": 30, "tibia": 0, "name": "right-front", "id": 1},
    2: {"coxia": 30, "femur": 30, "tibia": 0, "name": "left-front", "id": 2},
    3: {"coxia": 30, "femur": 30, "tibia": 0, "name": "left-middle", "id": 3},
    4: {"coxia": 30, "femur": 30, "tibia": 0, "name": "left-back", "id": 4},
    5: {"coxia": 30, "femur": 30, "tibia": 0, "name": "right-back", "id": 5},
    }
    pulses2servos = v2r.join_pose2pulse(coxia_femur_poses_deg)
    v2r.SendBusServoPulse(2000,pulses2servos)
    time.sleep(2)

    coxia_femur_tibia_poses_deg = {
    0: {"coxia": 30, "femur": 30, "tibia": 30, "name": "right-middle", "id": 0},
    1: {"coxia": 30, "femur": 30, "tibia": 30, "name": "right-front", "id": 1},
    2: {"coxia": 30, "femur": 30, "tibia": 30, "name": "left-front", "id": 2},
    3: {"coxia": 30, "femur": 30, "tibia": 30, "name": "left-middle", "id": 3},
    4: {"coxia": 30, "femur": 30, "tibia": 30, "name": "left-back", "id": 4},
    5: {"coxia": 30, "femur": 30, "tibia": 30, "name": "right-back", "id": 5},
    }
    pulses2servos = v2r.join_pose2pulse(coxia_femur_tibia_poses_deg)
    v2r.SendBusServoPulse(2000,pulses2servos)    
    time.sleep(2)
    # reset 
    pulses2servos = v2r.join_pose2pulse(v2r.nutural_poses_deg)
    v2r.SendBusServoPulse(2000,pulses2servos)
    time.sleep(2)
    
if __name__ == "__main__": 

    #TestNutualPositions()
    TestForwardKinematics()