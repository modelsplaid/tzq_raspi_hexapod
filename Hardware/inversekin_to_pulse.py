import sys
sys.path.append("../")
sys.path.append("../hexapod/ik_solver")

# inverse kinematics to real hexapod
import jointangle_to_pulse
import ik_solver2


# ********************************
# Dimensions
# ********************************

given_dimensions = {
    "front": 70,
    "side": 115,
    "middle": 120,
    "coxia": 60,
    "femur": 130,
    "tibia": 150,
}

# ********************************
# IK Parameters
# ********************************

given_ik_parameters = {
    "hip_stance": 7,
    "leg_stance": 32,
    "percent_x": 0.35,
    "percent_y": 0.25,
    "percent_z": -0.2,
    "rot_x": 2.5,
    "rot_y": -9,
    "rot_z": 14,
}


if __name__ == "__main__": 
    
    jointangle_to_pulse.TestForwardKinematics()

