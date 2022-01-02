from walkSequenceSolver import getWalkSequence
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
    "stepCount": 10.0,
    "hipSwing": 25.0,
    "liftSwing": 40.0,
}

getWalkSequence(dimensions, gaitParams)

