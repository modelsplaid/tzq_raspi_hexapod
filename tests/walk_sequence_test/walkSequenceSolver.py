from hexapodSolver import solveHexapodParams


def getHipSwingForward(aHipSwing):

    return {
        "left-front": -aHipSwing,
        "right-middle": aHipSwing,
        "left-back": -aHipSwing,
        "right-front": aHipSwing,
        "left-middle": -aHipSwing,
        "right-back": aHipSwing,
    }

def getHipSwingRotate(aHipSwing):

    return {
        "left-front": aHipSwing,
        "right-middle": aHipSwing,
        "left-back": aHipSwing,
        "right-front": aHipSwing,
        "left-middle": aHipSwing,
        "right-back": aHipSwing,
    }

def buildSequence(startVal, delta, stepCount):
    step = delta / stepCount

    currentItem = startVal
    array = []

    for i in range(stepCount):
        currentItem += step
        array = array+[currentItem]

    return array

def buildTripodSequences(startPose, aLiftSwing, hipSwings, stepCount, walkMode):
    #print("building tripod sequences ...")
    #print("pose: " +str(pose) )
    #print("aLiftSwing: " +str(aLiftSwing))
    
    doubleStepCount = 2 * stepCount
    #const legPositions = Object.keys(startPose)


    forwardAlphaSeqs = []
    liftBetaSeqs = []
    liftGammaSeqs = []
    for legPositionsIndex in startPose:
        alpha = startPose[legPositionsIndex]['coxia']
        beta = startPose[legPositionsIndex]['femur']
        gamma = startPose[legPositionsIndex]['tibia']
        leg_name = startPose[legPositionsIndex]['name']
        deltaApha = deltaAlpha = hipSwings[leg_name]
        print(deltaApha)
        # the sequence is not right : todo :check it out
        # 25.0
        #25.0
        #-25.0
        #-25.0
        #-25.0
        #25.0


def tripodSequence(pose, aLiftSwing, hipSwings, stepCount, walkMode):
    buildTripodSequences(pose, aLiftSwing, hipSwings, stepCount, walkMode)

def rippleSequence(startPose, aLiftSwing, hipSwings, stepCount):    
    b = 0

def getWalkSequence(dimensions,params,gaitType = "tripod",walkMode = "walking"):
    print("in getWalkSequence") 


    # initial value
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
    
    # assign user specified value
    rawIKparams["hip_stance"] = params["hipStance"]
    rawIKparams["leg_stance"] = params["legStance"]
    rawIKparams["percent_x"] = params["tx"]
    rawIKparams["percent_z"] = params["tz"]
    rawIKparams["rot_x"] =  params["rx"]
    rawIKparams["rot_y"] =  params["ry"]

    ikSolver_poses = solveHexapodParams(dimensions, rawIKparams)

    ahipSwing = abs(params["hipSwing"])
    aliftSwing = abs(params["liftSwing"])
    stepCount = params["stepCount"]

    aHipSwing = params["hipSwing"]
    if walkMode == "rotating":
        hipSwings = getHipSwingRotate(aHipSwing)
    else:    
        hipSwings = getHipSwingForward(aHipSwing)

    if gaitType == "ripple":
        rippleSequence(ikSolver_poses,aliftSwing,hipSwings, stepCount,walkMode)
    else: 
        tripodSequence(ikSolver_poses,aliftSwing,hipSwings, stepCount,walkMode)

