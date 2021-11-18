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

    # If servo rotation direction same as model joint angle, set 1
    # if opposite set -1.   
    # todo: here
    direction_poses_pulse = {
    0: {"coxia": 1, "femur": 1, "tibia": 1, "name": "right-middle", "id": 0},
    1: {"coxia": 1, "femur": 1, "tibia": 1, "name": "right-front", "id": 1},
    2: {"coxia": 1, "femur": 1, "tibia": 1, "name": "left-front", "id": 2},
    3: {"coxia": 1, "femur": 1, "tibia": 1, "name": "left-middle", "id": 3},
    4: {"coxia": 1, "femur": 1, "tibia": 1, "name": "left-back", "id": 4},
    5: {"coxia": 1, "femur": 1, "tibia": 1, "name": "right-back", "id": 5},
    }

    # joint of our hexa model has different  ids with the real-world servo 
    # each entry stands for corresponding servo id
    id_poses_pulse = {
    0: {"coxia": 13, "femur": 14, "tibia": 15, "name": "right-middle", "id": 0},
    1: {"coxia": 16, "femur": 17, "tibia": 18, "name": "right-front", "id": 1},
    2: {"coxia": 7, "femur": 8, "tibia": 9, "name": "left-front", "id": 2},
    3: {"coxia": 4, "femur": 5, "tibia": 6, "name": "left-middle", "id": 3},
    4: {"coxia": 1, "femur": 2, "tibia": 3, "name": "left-back", "id": 4},
    5: {"coxia": 10, "femur": 11, "tibia": 12, "name": "right-back", "id": 5},
    }
  
