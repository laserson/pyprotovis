import math

identity = lambda x: return x
index = lambda: return self.index
child = lambda: return self.childIndex
parent = lambda: return self.parent.index

def log(x,b=10):
    return math.log(x)/math.log(b)

def logFloor(x,b):
    return b**(math.floor(log(x,b))) if x > 0 else -(b**(-math.floor(-log(-x,b))))

def logCeil(x,b):
    return b**(math.ceil(log(x,b))) if x > 0 else -(b**(-math.ceil(-log(-x,b))))
