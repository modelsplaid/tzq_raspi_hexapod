from copy import deepcopy
from hexapod.plotter import HexapodPlotter
from hexapod.models import VirtualHexapod, Hexagon, Linkage
from hexapod.templates.figure_template import HEXAPOD_FIGURE
from hexapod.templates.pose_template import HEXAPOD_POSE
import sys
sys.path.append("../../")
try: 
    from Hardware import jointangle_to_pulse
except: 
    print("Hardware not found")

try:
    VIRTUAL_TO_REAL = jointangle_to_pulse.VirtualToReal()
except: 
    print("VIRTUAL_TO_REAL variable will not be created")
NAMES_LEG = Hexagon.VERTEX_NAMES
NAMES_JOINT = Linkage.POINT_NAMES

BASE_DIMENSIONS = {
    "front": 59,
    "side": 119,
    "middle": 93,
    "coxia": 45,
    "femur": 75,
    "tibia": 140,
}

BASE_IK_PARAMS = {
    "hip_stance": 0,
    "leg_stance": 0,
    "percent_x": 0,
    "percent_y": 0,
    "percent_z": 0,
    "rot_x": 0,
    "rot_y": 0,
    "rot_z": 0,
}

print("instance BASE_POSE")
BASE_POSE = deepcopy(HEXAPOD_POSE)

print("instance VirtualHexapod")
BASE_HEXAPOD = VirtualHexapod(BASE_DIMENSIONS)
print("--------instance BASE_PLOTTER")
BASE_PLOTTER = HexapodPlotter()

HEXAPOD = deepcopy(BASE_HEXAPOD)
HEXAPOD.update(HEXAPOD_POSE)
BASE_FIGURE = deepcopy(HEXAPOD_FIGURE)
BASE_PLOTTER.update(BASE_FIGURE, HEXAPOD)
