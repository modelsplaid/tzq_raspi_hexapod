from hexapodSolver import solveHexapodParams
from copy import deepcopy


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

    for i in range(int(stepCount)):
        currentItem += step
        array = array + [currentItem]

    return array


def buildTripodSequences(startPose, aLiftSwing, hipSwings, stepCount, walkMode):
    #print("building tripod sequences ...")
    #print("pose: " +str(pose) )
    #print("aLiftSwing: " +str(aLiftSwing))

    doubleStepCount = 2 * stepCount
    # const legPositions = Object.keys(startPose)

    forwardAlphaSeqs = {}
    liftBetaSeqs = {}
    liftGammaSeqs = {}
    for legPositionsIndex in startPose:
        alpha = startPose[legPositionsIndex]['coxia']
        beta = startPose[legPositionsIndex]['femur']
        gamma = startPose[legPositionsIndex]['tibia']
        leg_name = startPose[legPositionsIndex]['name']
        deltaApha = deltaAlpha = hipSwings[leg_name]
        #print("name: "+leg_name + "deltaAplpha: "+ str(deltaApha))

        # 1. build alpha sequence
        forwardAlpha = buildSequence(
            alpha - deltaAlpha,
            2 * deltaAlpha,
            doubleStepCount)
        forwardAlphaSeqs[leg_name] = forwardAlpha

        # 2. build beta  sequence
        liftBeta = buildSequence(beta, aLiftSwing, stepCount)
        liftBetaSeqs[leg_name] = liftBeta

        # 3. build gamma sequence
        liftGamma = buildSequence(gamma, -aLiftSwing / 2, stepCount)
        liftGammaSeqs[leg_name] = liftGamma

    return [forwardAlphaSeqs, liftBetaSeqs, liftGammaSeqs]

def tripodASequence(forwardAlphaSeqs,liftGammaSeqs,
                    liftBetaSeqs,doubleStepCount): 

    current_poses = {
        0: {
            "name": "right-middle",
            "id": 0,
            "coxia": [],
            "femur": [],
            "tibia": [],
        },       
        2: {
            "name": "left-front",
            "id": 2,
            "coxia": [],
            "femur": [],
            "tibia": [],
        },
        4: {
            "name": "left-back",
            "id": 4,
            "coxia": [],
            "femur": [],
            "tibia": [],
        },
    }

    for id_num in current_poses:
        
        #print("id_num name---" + str(current_poses[id_num]["name"]))

        # 1. generating alpha sequences (coxia)
        alpha = forwardAlphaSeqs[current_poses[id_num]["name"]]
        alpha_rev = deepcopy(alpha)
        alpha_rev.reverse()
        alpha = alpha + alpha_rev 
        current_poses[id_num]["coxia"] = alpha 
    
        # 2. generating beta sequences (femur)
        beta = liftBetaSeqs[current_poses[id_num]["name"]]
        beta_rev = deepcopy(beta)
        beta_rev.reverse()
        fillArrayBeta = [beta[0]]*int(doubleStepCount)
        beta = beta+beta_rev+fillArrayBeta
        current_poses[id_num]["femur"] = beta

        # 3. generating gamma sequences (tibia)

        gamma = liftGammaSeqs[current_poses[id_num]["name"]]
        gamma_rev = deepcopy(gamma)
        gamma_rev.reverse()
        fillArrayGamma = [gamma[0]]*int(doubleStepCount)
        gamma = gamma+gamma_rev+fillArrayGamma
        current_poses[id_num]["tibia"] = gamma

    #print("---current_poses")
    #print(current_poses)
    #print("forwardAlphaSeqs: ")
    #print(forwardAlphaSeqs)
    return current_poses

def tripodBSequence(forwardAlphaSeqs,liftGammaSeqs,
                    liftBetaSeqs,doubleStepCount): 

    current_poses = {
     
        1: {
            "name": "right-front",
            "id": 1,
            "coxia": [],
            "femur": [],
            "tibia": [],
        },
       
        3: {
            "name": "left-middle",
            "id": 3,
            "coxia": [],
            "femur": [],
            "tibia": [],
        },
       
        5: {
            "name": "right-back",
            "id": 5,
            "coxia": [],
            "femur": [],
            "tibia": [],
        },
    }


    for id_num in current_poses:
        
        #print("id_num name---" + str(current_poses[id_num]["name"]))

        # 1. generating alpha sequences (coxia)
        alpha = forwardAlphaSeqs[current_poses[id_num]["name"]]
        alpha_rev = deepcopy(alpha)
        alpha_rev.reverse()
        alpha = alpha_rev + alpha 
        current_poses[id_num]["coxia"] = alpha 
    
        # 2. generating beta sequences (femur)
        beta = liftBetaSeqs[current_poses[id_num]["name"]]
        beta_rev = deepcopy(beta)
        beta_rev.reverse()
        fillArrayBeta = [beta[0]]*int(doubleStepCount)
        beta = fillArrayBeta + beta+beta_rev
        current_poses[id_num]["femur"] = beta

        # 3. generating gamma sequences (tibia)

        gamma = liftGammaSeqs[current_poses[id_num]["name"]]
        gamma_rev = deepcopy(gamma)
        gamma_rev.reverse()
        fillArrayGamma = [gamma[0]]*int(doubleStepCount)
        gamma = fillArrayGamma+gamma+gamma_rev
        current_poses[id_num]["tibia"] = gamma

    #print("---current_poses")
    #print(current_poses)
    #print("forwardAlphaSeqs: ")
    #print(forwardAlphaSeqs)   
    return current_poses 

def tripodSequence(pose, aLiftSwing, hipSwings, stepCount, walkMode):
    [forwardAlphaSeqs, liftBetaSeqs, liftGammaSeqs] = buildTripodSequences(
                                                        pose, 
                                                        aLiftSwing, 
                                                        hipSwings, 
                                                        stepCount, 
                                                        walkMode)

    doubleStepCount = stepCount * 2 

    tripodA = tripodASequence(forwardAlphaSeqs,liftGammaSeqs,
                    liftBetaSeqs,doubleStepCount)    
    
    tripodB = tripodBSequence(forwardAlphaSeqs,liftGammaSeqs,
                    liftBetaSeqs,doubleStepCount)                                                                          
    
    tripodFull = tripodA.update(tripodB)
    tripodFull = deepcopy(tripodA)
    #print("---forwardAlphaSeqs: ")                                                        
    #print(forwardAlphaSeqs)        
    #print("---liftBetaSeqs: ")                                                        
    #print(liftBetaSeqs)
    #print("---liftGammaSeqs: ")                                                        
    #print(liftGammaSeqs)    
    #print("---tripodFull: ")
    #print(tripodFull)    
        
    return tripodFull


def rippleSequence(startPose, aLiftSwing, hipSwings, stepCount):
    b = 0


def getWalkSequence(dimensions, params, gaitType="tripod", walkMode="walking"):
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
    rawIKparams["rot_x"] = params["rx"]
    rawIKparams["rot_y"] = params["ry"]

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
        fullSequences = rippleSequence(ikSolver_poses, aliftSwing, hipSwings, stepCount, walkMode)
    else:
        fullSequences = tripodSequence(ikSolver_poses, aliftSwing, hipSwings, stepCount, walkMode)

    return fullSequences