import re

class Format(object):
    """Abstract"""
    
    quoted_re = re.compile(r'[\\\^\$\*\+\?\[\]\(\)\.\{\}]')
    
    def __init__(self):
        pass
    
    def re(self,s):
        (s_new,n) = self.quoted_re.subn(s)
        return s_new
    
    def pad(self,c,n,s):
        m = n - len(s)
        if m <= 0:
            return s
        else:
            return c*m + s

class date(Format):
    
    def format(self,d):
        def switch