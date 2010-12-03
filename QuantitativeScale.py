import numbers

import pyprotovis as pv
import Scale

class quantitative(Scale):
    """docstring for quantitative"""
    def __init__(self, arg):
        Scale.__init__()
        self.d = [0, 1] # default domain
        self.l = [0, 1] # default transformed domain
        self.r = [0, 1] # default range
        self.i = [pv.identity]  # default interpolators
        self.type = numbers.Number  # default type
        self.n = False  # whether the domain is negative
        self.f = pv.identity    # default forward transform
        self.g = pv.identity    # default inverse transform
        self.tickFormat = str   # default tick formatting fn
        return self
    
    @staticmethod
    def newDate(x):
        raise NotImplementedError
    
    def 
        