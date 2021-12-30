from hexapodSolver import solveHexapodParams



#const getHipSwingForward = aHipSwing => {
#    return {
#        leftFront: -aHipSwing,
#        rightMiddle: aHipSwing,
#        leftBack: -aHipSwing,
#        rightFront: aHipSwing,
#        leftMiddle: -aHipSwing,
#        rightBack: aHipSwing,
#    }
#}

#const getHipSwingRotate = aHipSwing => {
#    return {
#        leftFront: aHipSwing,
#        rightMiddle: aHipSwing,
#        leftBack: aHipSwing,
#        rightFront: aHipSwing,
#        leftMiddle: aHipSwing,
#        rightBack: aHipSwing,
#    }
#}

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

    ikSolver_poses = solveHexapodParams(dimensions, rawIKparams)

    ahipSwing = abs(params["hipSwing"])
    aliftSwing = abs(params["aliftSwing"])

    #const hipSwings =
    #walkMode === "rotating"
    #    ? getHipSwingRotate(aHipSwing)
    #    : getHipSwingForward(aHipSwing)