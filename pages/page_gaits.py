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

