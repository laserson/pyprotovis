import re

class Format(object):
    """Abstract"""
    
    quoted_re = re.compile(r'[\\\^\$\*\+\?\[\]\(\)\.\{\}]')
    
    def __init__(self):
        pass
    
    def re(self,s):
        re.
        