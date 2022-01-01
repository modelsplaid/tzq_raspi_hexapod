

def buildSequence(startVal, delta, stepCount):
    step = delta / stepCount

    currentItem = startVal
    array = []

    for i in range(stepCount):
        currentItem += step
        array = array+[currentItem]

    return array


if __name__ == '__main__':
    a = buildSequence(10,90,10)
    print(a)