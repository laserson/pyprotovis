import numbers

import Color

class Scale(object):
    """Abstract base class for Scales"""
    def __init__(self):
        pass
    
    @staticmethod
    def interpolator(start,end):
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