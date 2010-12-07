import math
import types
import numbers
import bisect

import pyprotovis as pv
import pyprotovis.Format
import Color

class Scale(object):
    """Abstract base class for Scales"""
    def __init__(self):
        pass
    
    def interpolator(self,start,end):
        """Returns fn that interpolates between given values"""
        if isinstance(start,numbers.Number):
            return lambda t: t * (end - start) + start
        
        # otherwise, assume color
        start = Color.color(start)
        end = Color.color(end)
        def _interp(t):
            a = start.a * (1 - t) + end.a * t
            if (a < 1e-5): a = 0
            if start.a == 0:
                return Color.rgb(end.r,end.g,end.b,a)
            elif end.a == 0:
                return Color.rgb(start.r,start.g,start.b,a)
            else:
                return Color.rgb(
                                  round(start.r * (1 - t) + end.r * t),
                                  round(start.g * (1 - t) + end.g * t),
                                  round(start.b * (1 - t) + end.b * t),
                                  a)
        return _interp
    
    def by(self,f):
        pass

class quantitative(Scale):
    """Implement abstract quantitative scale."""
    def __init__(self, *args):
        Scale.__init__(self)
        self._domain = [0,1]
        self._transformed_domain = [0,1]
        self._range  = [0,1]
        self._interpolators = [pv.identity]
        self._type = numbers.Number
        self._negative = False
        self._forward = pv.identity
        self._inverse = pv.identity
        self._tickFormat = str
        
        self.domain(*args)
        return self
    
    def scale(self,x):
        j = bisect.bisect_left(self._domain,x)
        j = max(0, min(len(self._interpolators) - 1, j))
        return self._interpolators[j]((self._forward(x) - self._transformed_domain[j]) / (self._transformed_domain[j + 1] - self._transformed_domain[j]))
    
    def __call__(self,x):
        return self.scale(x)
    
    def transform(self,forward,inverse):
        self._forward = lambda x: -forward(-x) if self._negative else forward(x)
        self._inverse = lambda y: -inverse(-x) if self._negative else inverse(x)
    
    def domain(self,*args):
        if len(args) == 0:
            return self._domain
        else:   # we were given arguments
            try:
                iter(args[0])   # if args[0] is iterable type
                array = args[0] # get array value
                if len(args) > 1:   # get accessors
                    min_accessor = args[1]
                if len(args) > 2:
                    max_accessor = args[2]
                if len(args) > 3:
                    raise ValueError, "If first arg is array type, can only provide two accessor fns"
                self._domain = [min(map(min_accessor,array)),max(map(max_accessor,array))] if len(array) > 0 else []
            except TypeError:   # else, args are values
                self._domain = args
            
            # check some exceptional cases:
            if len(self._domain) == 0:
                self._domain = [-float('inf'),float('inf')]
            elif len(self._domain) == 1:
                self._domain = [self._domain[0],self._domain[0]]
            
            self._negative = True if ((self._domain[0] < 0) or (self._domain[-1] < 0)) else False
            self._transformed_domain = map(self._forward,self._domain)
            
            return self
    
    def range(self,*args):
        if len(args) == 0:
            return self._range
        else:
            self._range = args
            
            # check some exceptional cases:
            if len(self._range) == 1:
                self._range = [self._range[0],self._range[1]]
            
            self._interpolators = []
            for i in xrange(len(self._range) - 1):
                self._interpolators.append(self.interpolator(self._range[i],self._range[i+1]))
            
            return self
    
    def invert(self,y):
        j = bisect.bisect_left(self._range,y)
        j = max(0, min(len(self._interpolators)-1, j))
        return self._inverse(self._transformed_domain[j] + (y - self._range[j]) / (self._range[j+1] - self._range[j]) * (self._transformed_domain[j+1] - self._transformed_domain[j]))
    
    def ticks(self,m=10):
        start = self._domain[0]
        end   = self._domain[-1]
        reverse = end < start
        _min = float(end if reverse else start)
        _max = float(start if reverse else end)
        span = _max - _min
        
        # test special degenerate cases
        if span == 0 or math.isinf(span):
            return _min
        
        step = pv.logFloor(span / m, 10)
        err = m / (span / step)
        if err <= 0.15: step *= 5
        if err <= 0.75: step *= 2
        start =  math.ceil(_min / step) * step
        end   = math.floor(_min / step) * step
        self._tickFormat = pv.Format.number().fractionDigits( max(0, math.floor(pv.log(step,10) + 0.01)) )
        ticks = range(start, end + step, step)
        
        return reversed(ticks) if reverse else ticks
    
    def tickFormat(self,t):
        return self._tickFormat(t)
    
    def nice(self):
        if len(self._domain != 2): return self  # no support for non-uniform domains
        start = self._domain[0]
        end   = self._domain[-1]
        reverse = end < start
        _min = float(end if reverse else start)
        _max = float(start if reverse else end)
        span = _max - _min
        
        # test special degenerate cases
        if span == 0 or math.isinf(span):
            return _min
        
        step = 10**(round(math.log10(span)) - 1)
        self._domain = [math.floor(_min / step) * step, math.ceil(_max / step) * step]
        if reverse: self._domain.reverse()
        self._transformed_domain = map(self._forward,self._domain)
        
        return self
    
    def by(self,f):
        raise NotImplementedError

# NOTE: linear class is equiv to default implementation of quantitative
linear = quantitative

class log(quantitative):
    """Implementation of log scale"""
    def __init__(self, *args):
        quantitative.__init__(self,1,10)
        self.arg = arg
        