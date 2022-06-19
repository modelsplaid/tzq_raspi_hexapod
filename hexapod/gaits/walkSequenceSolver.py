import sys
sys.path.append("../../")
from hexapod.gaits.hexapodSolver import solveHexapodParams
from copy import deepcopy
import numpy as np
import pprint
def getHipSwingForward(aHipSwing):

    return {
        "left-front": -aHipSwing,
        "right-middle": aHipSwing,
        "left-back": -aHipSwing,
        "right-front": aHipSwing,
        "left-middle": -aHipSwing,
        "right-back": aHipSwing,
    }

# backward
def getHipSwingBackward(aHipSwing):

    return {
        "left-front": aHipSwing,
        "right-middle": -aHipSwing,
        "left-back": aHipSwing,
        "right-front": -aHipSwing,
        "left-middle": aHipSwing,
        "right-back": -aHipSwing,
    }

# rotate right
def getHipSwingRotateRight(aHipSwing):

    return {
        "left-front": -aHipSwing,
        "right-middle": -aHipSwing,
        "left-back": -aHipSwing,
        "right-front": -aHipSwing,
        "left-middle": -aHipSwing,
        "right-back": -aHipSwing,
    }

# rotate left
def getHipSwingRotateLeft(aHipSwing):

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
        alpha = alpha + alpha_rev[1:] 
        current_poses[id_num]["coxia"] = alpha 
    
        # 2. generating beta sequences (femur)
        beta = liftBetaSeqs[current_poses[id_num]["name"]]
        beta_rev = deepcopy(beta)
        beta_rev.reverse()
        fillArrayBeta = [beta[0]]*(int(doubleStepCount)-1)
        beta = beta+beta_rev+fillArrayBeta
        current_poses[id_num]["femur"] = beta

        # 3. generating gamma sequences (tibia)

        gamma = liftGammaSeqs[current_poses[id_num]["name"]]
        gamma_rev = deepcopy(gamma)
        gamma_rev.reverse()
        fillArrayGamma = [gamma[0]]*(int(doubleStepCount)-1)
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
        alpha = alpha_rev + alpha[1:] 
        current_poses[id_num]["coxia"] = alpha 
    
        # 2. generating beta sequences (femur)
        beta = liftBetaSeqs[current_poses[id_num]["name"]]
        beta_rev = deepcopy(beta)
        beta_rev.reverse()
        fillArrayBeta = [beta[0]]*(int(doubleStepCount)-1)
        beta = fillArrayBeta + beta+beta_rev
        current_poses[id_num]["femur"] = beta

        # 3. generating gamma sequences (tibia)

        gamma = liftGammaSeqs[current_poses[id_num]["name"]]
        gamma_rev = deepcopy(gamma)
        gamma_rev.reverse()
        fillArrayGamma = [gamma[0]]*(int(doubleStepCount)-1)
        gamma = fillArrayGamma+gamma+gamma_rev
        current_poses[id_num]["tibia"] = gamma

    #print("---current_poses")
    #print(current_poses)
    #print("forwardAlphaSeqs: ")
    #print(forwardAlphaSeqs)   
    return current_poses 


# right front leg will move first.
def tripodSequenceAdvanced(pose, aLiftSwing, hipSwings, stepCount, walkMode):
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
    tripodTmp = deepcopy(tripodA)                
    tripodTmp.update(tripodB)
    # extract first pose
    first_pose = deepcopy(pose)

    for id_key in first_pose:
        first_pose[id_key]["coxia"] = tripodTmp[id_key]["coxia"][0]
        first_pose[id_key]["femur"] = tripodTmp[id_key]["femur"][0]
        first_pose[id_key]["tibia"] = tripodTmp[id_key]["tibia"][0]

    # extract preA sequence
    left_front_key = 2
    left_front_sqs = tripodA[left_front_key] # extrace all moving seqs for left front leg
    pprint.pprint("+++++left_front_sqs:"+str(left_front_sqs))
    coxia_sqs = left_front_sqs["coxia"]
    femur_sqs = left_front_sqs["femur"]
    tibia_sqs = left_front_sqs["tibia"]
    len_coxia_sqs = len(coxia_sqs) 
   
    #Append this move sequence as an independant move poses
    pre_coxia_sqs = coxia_sqs[0:int((len_coxia_sqs-1)/2)]
    pre_femur_sqs = femur_sqs[0:int((len_coxia_sqs-1)/2)]
    pre_tibia_sqs = tibia_sqs[0:int((len_coxia_sqs-1)/2)]
    len_pre_sqs = len(pre_coxia_sqs)
    preFullPoses = deepcopy(pose)

    #Generating static posels
    for legPositionsIndex in first_pose:

        alpha =    first_pose[legPositionsIndex]['coxia']
        beta =     first_pose[legPositionsIndex]['femur']
        gamma =    first_pose[legPositionsIndex]['tibia']
        leg_name = first_pose[legPositionsIndex]['name']

        preFullPoses[legPositionsIndex]['coxia'] = [alpha]*len_pre_sqs
        preFullPoses[legPositionsIndex]['femur'] = [beta]*len_pre_sqs
        preFullPoses[legPositionsIndex]['tibia'] = [gamma]*len_pre_sqs
    # Append pre seqs
    preFullPoses[left_front_key]['coxia'] = pre_coxia_sqs
    preFullPoses[left_front_key]['femur'] = pre_femur_sqs
    preFullPoses[left_front_key]['tibia'] = pre_tibia_sqs

    #pprint.pprint("++++++ preFullPoses: " )
    #pprint.pprint( preFullPoses)
    #pprint.pprint("+++++tripodA:"+str(tripodA))
    #pprint.pprint("+++++tripodB:"+str(tripodB))
   
    # Generating post poses
    postFullPoses = deepcopy(tripodTmp)

    for i in range(len_pre_sqs):
        postFullPoses[left_front_key]['coxia'][i] = pre_coxia_sqs[-1]
        postFullPoses[left_front_key]['femur'][i] = pre_femur_sqs[-1]
        postFullPoses[left_front_key]['tibia'][i] = pre_tibia_sqs[-1]
    
    # remove first and  last pose, since it is the same as first pose
    for id_key in postFullPoses:
        postFullPoses[id_key]["coxia"] = postFullPoses[id_key]["coxia"][1:-1]
        postFullPoses[id_key]["femur"] = postFullPoses[id_key]["femur"][1:-1]
        postFullPoses[id_key]["tibia"] = postFullPoses[id_key]["tibia"][1:-1]

    # append pre and post poses   
    for id_key in postFullPoses:
        postFullPoses[id_key]["coxia"] = preFullPoses[id_key]['coxia']+postFullPoses[id_key]["coxia"]
        postFullPoses[id_key]["femur"] = preFullPoses[id_key]['femur']+postFullPoses[id_key]["femur"]
        postFullPoses[id_key]["tibia"] = preFullPoses[id_key]['tibia']+postFullPoses[id_key]["tibia"]

    fullPoses = deepcopy(postFullPoses)
    return  fullPoses


# right front leg will move first.
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

    pprint.pprint("+++++tripodA:"+str(tripodA))
    pprint.pprint("+++++tripodB:"+str(tripodB))    
    tripodA.update(tripodB)
    tripodFull = deepcopy(tripodA)
 
    # remove last pose, since it is the same as first pose
    for id_key in tripodFull:
        tripodFull[id_key]["coxia"] = tripodFull[id_key]["coxia"][0:-1]
        tripodFull[id_key]["femur"] = tripodFull[id_key]["femur"][0:-1]
        tripodFull[id_key]["tibia"] = tripodFull[id_key]["tibia"][0:-1]
        
    return tripodFull

def modSequence(mod, seq):
    #const sequence = [...seq, ...seq]
    #//console.log("---sequence: ")
    #//console.log(sequence)

    #return sequence.slice(mod, mod + 6).flat()
    sequence = seq + seq
    sequence_np = np.array(sequence)        
    sequenceModNp = sequence_np[mod:mod+6]
    seqFlattenNp = sequenceModNp.flatten()
    sequenceModList = seqFlattenNp.tolist()
    
    return sequenceModList

def buildRippleLegSequence(position, bLift, gLift, fw1, fw2, bk1, bk2, bk3, bk4):
    stepCount = len(fw1)
    revGLift = deepcopy(gLift)
    revGLift.reverse()

    revBLift = deepcopy(bLift)
    revBLift.reverse()

    b0 = bLift[0]
    g0 = gLift[0]

    bN = [b0] * stepCount
    gN = [g0] * stepCount

    alphaSeq = [fw1]+[fw2]+[bk1]+[bk2]+[bk3]+[bk4]
    betaSeq = [bLift]+[revBLift]+[bN]+[bN]+[bN]+[bN]
    gammaSeq = [gLift]+[revGLift]+[gN]+[gN]+[gN]+[gN]


    moduloMap = {
        "left-back": 0,
        "right-front": 1,
        "left-middle": 2,
        "right-back": 3,
        "left-front": 4,
        "right-middle": 5,
    }

    alpha = modSequence(moduloMap[position], alphaSeq) # todo here
    beta = modSequence(moduloMap[position], betaSeq)
    gamma = modSequence(moduloMap[position], gammaSeq)
       
    return [alpha,beta,gamma]

def rippleSequence(startPose, aLiftSwing, hipSwings, stepCount, walkMode):
    print("In ripple sequence")

    sequences = {
        0: {
            "name": "right-middle",
            "id": 0,
            "coxia": [],
            "femur": [],
            "tibia": [],
        },
        1: {
            "name": "right-front",
            "id": 1,
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
        3: {
            "name": "left-middle",
            "id": 3,
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
        5: {
            "name": "right-back",
            "id": 5,
            "coxia": [],
            "femur": [],
            "tibia": [],
        },
    }

    betaLift = []
    gammaLift = []
    for legPositionsIndex in startPose:
        #print("legPositionsIndex")
        #print(legPositionsIndex)
        alpha = startPose[legPositionsIndex]['coxia']
        beta = startPose[legPositionsIndex]['femur']
        gamma = startPose[legPositionsIndex]['tibia']

        legPositionName = startPose[legPositionsIndex]['name']
        delta = hipSwings[legPositionName]
        halfDelta = delta / 2.0
        # 1. build beta sequence
        betaLift = buildSequence(beta, aLiftSwing, stepCount)
        gammaLift = buildSequence(gamma, -aLiftSwing / 2.0, stepCount)

        fw1 = buildSequence(alpha - delta, delta, stepCount)
        fw2 = buildSequence(alpha, delta, stepCount)

        bk1 = buildSequence(alpha + delta, -halfDelta, stepCount)
        bk2 = buildSequence(alpha + halfDelta, -halfDelta, stepCount)
        bk3 = buildSequence(alpha, -halfDelta, stepCount)
        bk4 = buildSequence(alpha - halfDelta, -halfDelta, stepCount)

        [alpha,beta,gamma] = buildRippleLegSequence(legPositionName, 
                betaLift, gammaLift, fw1, fw2, bk1, bk2, bk3, bk4)

        sequences[legPositionsIndex]['coxia'] = alpha
        sequences[legPositionsIndex]['femur'] = beta
        sequences[legPositionsIndex]['tibia'] = gamma
        
        #print("---sequences[legPositionName]: " +str(legPositionName)  )                
        #print(sequences[legPositionName])
    return sequences

def getWalkSequence(dimensions, params, gaitType="tripod", walkMode="walking"):
    #walkMode options: "walkingforward" "walkingbackward" "rotatingleft" "rotatingright"
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
    if walkMode == "rotatingleft":
        hipSwings = getHipSwingRotateLeft(aHipSwing)
    elif walkMode == "rotatingright":
        hipSwings = getHipSwingRotateRight(aHipSwing)
    elif walkMode == "walkingforward" :
        hipSwings = getHipSwingForward(aHipSwing)
    elif walkMode == "walkingbackward" :
        hipSwings = getHipSwingBackward(aHipSwing)

    if gaitType == "ripple":
        fullSequences = rippleSequence(ikSolver_poses, aliftSwing, hipSwings, stepCount, walkMode)
    else:
        fullSequences = tripodSequence(ikSolver_poses, aliftSwing, hipSwings, stepCount, walkMode)
        fullSequencesAdvanced = tripodSequenceAdvanced(ikSolver_poses, aliftSwing, hipSwings, stepCount, walkMode)
        # todo here: append pre and post sqs
        #pprint.pprint("++++++fullSequences: ")
        #pprint.pprint(fullSequences)
    return fullSequencesAdvanced


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

    print("walk_seq[0]['coxia']" +str(walk_seq[0]['coxia']))
    return poses_deg

