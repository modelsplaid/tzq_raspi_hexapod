
def solveHexapodParams(dimensions, rawIKparams, true): 
    a = 0

def getWalkSequence(dimensions,params,gaitType = "tripod",walkMode = "walking"):
    print("in getWalkSequence") 

    rawIKparams = {
        "hip_stance": 0,
        "leg_stance": 0,
        "percent_x": 0.0,
        "percent_y": 0.0,
        "percent_z": 0.0,
        "rot_x": 0,
        "rot_y": 0,
        "rot_z": 0,
    }
   
    rawIKparams["hip_stance"] = params["hipStance"]
    rawIKparams["leg_stance"] = params["legStance"]
    rawIKparams["percent_x"] = params["tx"]
    rawIKparams["percent_z"] = params["tz"]
    rawIKparams["rot_x"] = params["rx"]
    rawIKparams["rot_y"] = params["ry"]

    #const [ikSolver] = solveHexapodParams(dimensions, rawIKparams, true)