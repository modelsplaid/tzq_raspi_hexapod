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

class VirtualToReal:
    
    #Number of pulses needed to rotate one degree 
    pulses_per_deg = 395.0/90.0

    #Number of degrees needed to rotate one pulse
    degs_per_pulse = 1.0/pulses_per_deg
    
    # Pulses for each servo when alpha beta and gamma all equal to one
    nutural_poses_pulse = {
    0: {"coxia": -40, "femur": 19, "tibia": 6, "name": "right-middle", "id": 0},
    1: {"coxia": 33, "femur": 85, "tibia": -60, "name": "right-front", "id": 1},
    2: {"coxia": -20, "femur": 90, "tibia": -13, "name": "left-front", "id": 2},
    3: {"coxia": -12, "femur": -25, "tibia": 3, "name": "left-middle", "id": 3},
    4: {"coxia": 0, "femur": 94, "tibia": -70, "name": "left-back", "id": 4},
    5: {"coxia": -5, "femur": 17, "tibia": 2, "name": "right-back", "id": 5},
    }

  
