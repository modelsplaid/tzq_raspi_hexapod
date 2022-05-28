import json 


def dum_config():
    dict_json = {'NUTURAL_POSES_PULSE': NUTURAL_POSES_PULSE,\
            'NUTURAL_POSES_DEG': NUTURAL_POSES_DEG,\
            'DIRECTION_POSES_PULSE': DIRECTION_POSES_PULSE,\
            'SERVO_ID_MAPPING':SERVO_ID_MAPPING,
            'PULSES2SERVOS':PULSES2SERVOS      
            }

    out_file = open("const_hardware_config.json", "w") 
    json.dump(dict_json,out_file,indent = 4) 
    print("IN const hardware:  ")
    #print(NUTURAL_POSES_PULSE)    



out_file = open("./config/const_hardware_config.json", "r")
config_json = json.load(out_file)
NUTURAL_POSES_PULSE = config_json['NUTURAL_POSES_PULSE']
NUTURAL_POSES_DEG = config_json['NUTURAL_POSES_DEG']
DIRECTION_POSES_PULSE = config_json['DIRECTION_POSES_PULSE']
SERVO_ID_MAPPING = config_json['SERVO_ID_MAPPING']
PULSES2SERVOS = config_json['PULSES2SERVOS']
print('-----------PULSES2SERVOS')
print(PULSES2SERVOS)
 

if __name__ == "__main__":
        out_file = open("../config/const_hardware_config.json", "r")
        config_json = json.load(out_file)
        NUTURAL_POSES_PULSE = config_json['NUTURAL_POSES_PULSE']
        NUTURAL_POSES_DEG = config_json['NUTURAL_POSES_DEG']
        DIRECTION_POSES_PULSE = config_json['DIRECTION_POSES_PULSE']
        SERVO_ID_MAPPING = config_json['SERVO_ID_MAPPING']
        PULSES2SERVOS = config_json['PULSES2SERVOS']

        print("NUTURAL_POSES_PULSE:")
        print(NUTURAL_POSES_PULSE)