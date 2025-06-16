def read_record():
    with open ("record","r",encoding="UTF-8") as rec:
        recor = rec.read()
    if len(recor) < 1:
        return 0
    return int(recor)

def ride_record(nop):

    with open  ("record","w",encoding="UTF-8") as rec:
        rec.write(str(nop))