def getWalkSequence(dimensions,params,gaitType = "tripod",walkMode = "walking"):
    print("in getWalkSequence") 

    ik_parameters = {
        "hip_stance": 25,
        "leg_stance": 0,
        "percent_x": 0.0,
        "percent_y": 0.0,
        "percent_z": 0.0,
        "rot_x": 0,
        "rot_y": 0,
        "rot_z": 0,
    }

    '''
     const { hipStance, rx, ry, tx, tz, legStance } = params
    const rawIKparams = {
        tx,
        ty: 0,
        tz,
        legStance,
        hipStance,
        rx,
        ry,
        rz: 0,
    }
    '''