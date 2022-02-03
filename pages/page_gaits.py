import json
#from types import NoneType

#from types import NoneType
from dash.dependencies import Output
from app import app
from settings import WHICH_POSE_CONTROL_UI
from hexapod.models import VirtualHexapod
from hexapod.const import BASE_PLOTTER
from pages import helpers, shared
from copy import deepcopy

import time
import sys
from widgets.gaits_ui import GAITS_WIDGETS_SECTION, GAITS_CALLBACK_INPUTS,GAITS_BUTTON_CALLBACK_INPUTS,RADIOS_CALLBACK_INPUTS

try:
    from hexapod.const import VIRTUAL_TO_REAL
except: 
    print("page_gaits running in simulator")
sys.path.append("../../")

from hexapod.gaits.walkSequenceSolver import getWalkSequence, extract_walkseqs
try:
    from Hardware import jointangle_to_pulse 
except: 
    print("import hardware failed! only running on simulator")


if WHICH_POSE_CONTROL_UI == 1:
    print("---1WHICH_POSE_CONTROL_UI: ")
    print(WHICH_POSE_CONTROL_UI)

    from widgets.pose_control.generic_daq_slider_ui import KINEMATICS_WIDGETS_SECTION
elif WHICH_POSE_CONTROL_UI == 2:
    print("---2WHICH_POSE_CONTROL_UI: ")
    print(WHICH_POSE_CONTROL_UI)

    from widgets.pose_control.generic_slider_ui import KINEMATICS_WIDGETS_SECTION
else:
    print("---else WHICH_POSE_CONTROL_UI: ")
    print(WHICH_POSE_CONTROL_UI)
    from widgets.pose_control.generic_input_ui import KINEMATICS_WIDGETS_SECTION

# ......................
# Page layout
# ......................
GRAPH_ID = "graph-gaits"
MESSAGE_SECTION_ID = "message-gaits"
PARAMETERS_SECTION_ID = "parameters-gaits"

sidebar = shared.make_standard_page_sidebar(
    MESSAGE_SECTION_ID, PARAMETERS_SECTION_ID, GAITS_WIDGETS_SECTION
)

layout = shared.make_standard_page_layout(GRAPH_ID, sidebar)

def process_gait_seq(gaitType = "ripple",walkMode = "walking"):

    dimensions = {
    "front": 59,
    "side": 119,
    "middle": 93,
    "coxia": 45,
    "femur": 75,
    "tibia": 140,
    }

    POSITION_NAMES_LIST = [
        "left-front",
        "right-middle",
        "left-back",
        "right-front",
        "left-middle",
        "right-back",
    ]

    gaitParams = {
        "tx": 0,
        "tz": 0,
        "rx": 0,
        "ry": 0,
        "legStance": 0,
        "hipStance": 25.0,
        "stepCount": 2.0,
        "hipSwing": 25.0,
        "liftSwing": 60.0,
    }

    
    #gaitType = "tripod"
    fullSequences = getWalkSequence(dimensions, gaitParams,gaitType,walkMode)
    #print("fullSequences: ")
    #print(fullSequences)
    return fullSequences


# ......................
# Update page
# ......................
outputs, inputs, states = shared.make_standard_page_callback_params(
    GRAPH_ID, PARAMETERS_SECTION_ID, MESSAGE_SECTION_ID
)

@app.callback(outputs, inputs, states)
def update_patterns_page(dimensions_json, poses_json, relayout_data, figure):
    global glo_step_counter
    print("in update_patterns_page")
    dimensions = helpers.load_params(dimensions_json, "dims")
    poses = helpers.load_params(poses_json, "pose")
    hexapod = VirtualHexapod(dimensions)



    try:
        hexapod.update(poses)
    except Exception as alert:
        return figure, helpers.make_alert_message(alert)

    BASE_PLOTTER.update(figure, hexapod)
    helpers.change_camera_view(figure, relayout_data)
    return figure, ""


# ......................
# Update parameters sliders
# ......................

output_parameter = Output(PARAMETERS_SECTION_ID, "children")
input_parameters = GAITS_CALLBACK_INPUTS
in_param_startstop_button = GAITS_BUTTON_CALLBACK_INPUTS
in_param_radios = RADIOS_CALLBACK_INPUTS
@app.callback(output_parameter, input_parameters,in_param_startstop_button,in_param_radios)
def update_poses_alpha_beta_gamma(
        hipSwing_val, liftSwing_val, hipStance_val,
        liftStance,stepCount,speed,
        buttonStartStop_nclicks,buttonKeepMov_nclicks,
        radio_gaittype,radio_movedir,radio_walkrot):
    
    print("buttonStartStop_nclicks: " +str(buttonStartStop_nclicks))        
    print("buttonKeepMov_nclicks: " +str(buttonKeepMov_nclicks))
    print("radio_gaittype: " +str(radio_gaittype))
    print("radio_movedir: " +str(radio_movedir))
    print("radio_walkrot: " +str(radio_walkrot))    
    
    one_pose = {
        0: {"coxia": 0, "femur": 0, "tibia": 0, "name": "right-middle", "id": 0},
        1: {"coxia": 0, "femur": 0, "tibia": 0, "name": "right-front", "id": 1},
        2: {"coxia": 0, "femur": 0, "tibia": 0, "name": "left-front", "id": 2},
        3: {"coxia": 0, "femur": 0, "tibia": 0, "name": "left-middle", "id": 3},
        4: {"coxia": 0, "femur": 0, "tibia": 0, "name": "left-back", "id": 4},
        5: {"coxia": 0, "femur": 0, "tibia": 0, "name": "right-back", "id": 5},
        }

    if(buttonStartStop_nclicks is not None):
        button_step_counter = buttonStartStop_nclicks
    else:
        button_step_counter = 0

    # tzq comment: the poses is where we need to send to real robot
    try:

        # generating gait sequences
        seqs = process_gait_seq(radio_gaittype,radio_walkrot)

        num_seqs =len(seqs[0]['coxia'])        

        print("num_seqs:"+str(num_seqs))
        print("button_step_counter:"+str(button_step_counter%num_seqs))
        one_pose = extract_walkseqs(seqs,button_step_counter%num_seqs)

        # send to real robot
        global VIRTUAL_TO_REAL
        pulses2servos = VIRTUAL_TO_REAL.update_puses(one_pose)
        VIRTUAL_TO_REAL.SendBusServoPulse(300,pulses2servos)
        time.sleep(0.3)
        #for i in range(num_seqs):
        #    one_pose = extract_walkseqs(seqs,i)
        #    print("one_pose:")
        #    print(one_pose)
        #    pulses2servos = VIRTUAL_TO_REAL.update_puses(one_pose)
        #    VIRTUAL_TO_REAL.SendBusServoPulse(300,pulses2servos)   
        #    time.sleep(0.3)

    except: 
        print("Page gaits running in simulator")

    return json.dumps(one_pose)

