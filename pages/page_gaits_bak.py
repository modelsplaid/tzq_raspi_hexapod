import json
from dash.dependencies import Output
from app import app
from settings import WHICH_POSE_CONTROL_UI
from hexapod.models import VirtualHexapod
from hexapod.const import BASE_PLOTTER
from widgets.pose_control.components import KINEMATICS_CALLBACK_INPUTS
from pages import helpers, shared
from copy import deepcopy

import time
import sys
try:
    from hexapod.const import VIRTUAL_TO_REAL
except: 
    print("page_gaits running in simulator")
sys.path.append("../../")

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
    MESSAGE_SECTION_ID, PARAMETERS_SECTION_ID, KINEMATICS_WIDGETS_SECTION
)
print("---sidebar")
print(sidebar)
layout = shared.make_standard_page_layout(GRAPH_ID, sidebar)

# ......................
# Update page
# ......................

outputs, inputs, states = shared.make_standard_page_callback_params(
    GRAPH_ID, PARAMETERS_SECTION_ID, MESSAGE_SECTION_ID
)

@app.callback(outputs, inputs, states)
def update_kinematics_page(dimensions_json, poses_json, relayout_data, figure):

    dimensions = helpers.load_params(dimensions_json, "dims")
    
    #print("---update kine page, dimensions_json: ")
    #print(dimensions_json)
    #print("---update kine page, dimensions: ")
    #print(dimensions)

    poses = helpers.load_params(poses_json, "pose")
    
    hexapod = VirtualHexapod(dimensions)

    #tzq comment: the poses is where we need to send to real robot
    try:
        global VIRTUAL_TO_REAL
        pulses2servos = VIRTUAL_TO_REAL.update_puses(poses)
        VIRTUAL_TO_REAL.SendBusServoPulse(300,pulses2servos)        
    except: 
        print("Page kinematics running in simulator")
    # tzq todo here
    try:
        hexapod.update(poses, assume_ground_targets=False)
    except Exception as alert:
        return figure, helpers.make_alert_message(alert)

    BASE_PLOTTER.update(figure, hexapod)
    helpers.change_camera_view(figure, relayout_data)


    return figure, ""


# ......................
# Update parameters
# ......................


output_parameter = Output(PARAMETERS_SECTION_ID, "children")
input_parameters = KINEMATICS_CALLBACK_INPUTS

# fmt: off


@app.callback(output_parameter, input_parameters)
def update_poses(
    rmc, rmf, rmt,
    rfc, rff, rft,
    lfc, lff, lft,
    lmc, lmf, lmt,
    lbc, lbf, lbt,
    rbc, rbf, rbt,
):

    return json.dumps({
        0: {"coxia": rmc or 0, "femur": rmf or 0, "tibia": rmt or 0, "name": "right-middle", "id": 0},
        1: {"coxia": rfc or 0, "femur": rff or 0, "tibia": rft or 0, "name": "right-front", "id": 1},
        2: {"coxia": lfc or 0, "femur": lff or 0, "tibia": lft or 0, "name": "left-front", "id": 2},
        3: {"coxia": lmc or 0, "femur": lmf or 0, "tibia": lmt or 0, "name": "left-middle", "id": 3},
        4: {"coxia": lbc or 0, "femur": lbf or 0, "tibia": lbt or 0, "name": "left-back", "id": 4},
        5: {"coxia": rbc or 0, "femur": rbf or 0, "tibia": rbt or 0, "name": "right-back", "id": 5},
    })

# fmt: on
