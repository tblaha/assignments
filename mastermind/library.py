n=4
k=6

def rightpos(code,userint):
    global n
    numrightpos=0
    lstrightpos=[]
    for i in range(n):
        if code[i] == userint[i]:
            numrightpos += 1
            lstrightpos.append(userint[i])
    return numrightpos,lstrightpos

def occurs(code,userint,lstrightpos):
    global n
    numoccurs=0
    for i in range(n):
        if code.count(userint[i]) and not lstrightpos.count(userint[i]):
            numoccurs += 1
    return numoccurs
