import json
from dash.dependencies import Output
from app import app
from settings import WHICH_POSE_CONTROL_UI
from hexapod.models import VirtualHexapod
from hexapod.const import BASE_PLOTTER
from pages import helpers, shared
from copy import deepcopy

import time
import sys
from widgets.gaits_ui import GAITS_WIDGETS_SECTION, GAITS_CALLBACK_INPUTS,GAITS_BUTTON_CALLBACK_INPUTS

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

def process_gait_seq():

    dimensions = {
    "front": 100,
    "side": 100,
    "middle": 100,
    "coxia": 100,
    "femur": 100,
    "tibia": 100,
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
        "liftSwing": 20.0,
    }

    gaitType = "ripple"
    fullSequences = getWalkSequence(dimensions, gaitParams,gaitType)
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
    print("in update_patterns_page")
    dimensions = helpers.load_params(dimensions_json, "dims")
    poses = helpers.load_params(poses_json, "pose")
    hexapod = VirtualHexapod(dimensions)




    # tzq comment: the poses is where we need to send to real robot
    try:
        global VIRTUAL_TO_REAL

        seqs = process_gait_seq()
        one_pose = extract_walkseqs(seqs,0)
        print("one_pose:")
        print(one_pose)
        pulses2servos = VIRTUAL_TO_REAL.update_puses(one_pose)
        VIRTUAL_TO_REAL.SendBusServoPulse(300,pulses2servos)   


    except: 
        print("Page kinematics running in simulator")

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

@app.callback(output_parameter, input_parameters,in_param_startstop_button)
def update_poses_alpha_beta_gamma(
        hipSwing_val, liftSwing_val, hipStance_val,
        liftStance,stepCount,speed,
        buttonStartStop_nclicks,buttonKeepMov_nclicks):
    print("buttonStartStop_nclicks: " +str(buttonStartStop_nclicks))    
    print("buttonKeepMov_nclicks: " +str(buttonKeepMov_nclicks))    



    
    return json.dumps(helpers.make_pose(hipSwing_val, liftSwing_val, hipStance_val))

