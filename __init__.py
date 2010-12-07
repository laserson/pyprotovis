import math

identity = lambda x: return x
index = lambda: return self.index
child = lambda: return self.childIndex
parent = lambda: return self.parent.index

def log(x,b=10):
    return math.log(x)/math.log(b)

def logFloor(x,b=10):
    return math.floor(log(x,b))
