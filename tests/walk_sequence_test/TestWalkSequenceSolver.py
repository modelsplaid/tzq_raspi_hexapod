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
    "stepCount": 2.0,
    "hipSwing": 25.0,
    "liftSwing": 20.0,
}

def extract_walkseqs(walk_seq,index_seq): 
    poses_deg = {
        0: {"coxia": 0, "femur": 0, "tibia": 0, "name": "right-middle", "id": 0},
        1: {"coxia": 0, "femur": 0, "tibia": 0, "name": "right-front", "id": 1},
        2: {"coxia": 0, "femur": 0, "tibia": 0, "name": "left-front", "id": 2},
        3: {"coxia": 0, "femur": 0, "tibia": 0, "name": "left-middle", "id": 3},
        4: {"coxia": 0, "femur": 0, "tibia": 0, "name": "left-back", "id": 4},
        5: {"coxia": 0, "femur": 0, "tibia": 0, "name": "right-back", "id": 5},
        }

    num_legs = len(walk_seq)
    for i in range(num_legs):

        poses_deg[i]['coxia'] = walk_seq[i]['coxia'][index_seq]
        poses_deg[i]['femur'] = walk_seq[i]['femur'][index_seq]
        poses_deg[i]['tibia'] = walk_seq[i]['tibia'][index_seq]

    return poses_deg



gaitType = "ripple"
fullSequences = getWalkSequence(dimensions, gaitParams,gaitType)
print("fullSequences[0]['coxia'][0]: " + str(fullSequences[0]['coxia'][0]))
print("number of walk sequences: " + str(len(fullSequences[0]['coxia'])))

extracted_seq = extract_walkseqs(fullSequences,0)
print("extracted_seq: ")
print(extracted_seq)
