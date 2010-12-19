class Mark(object):
    """Abstract Mark class"""
    def __init__(self, *arg):
        self.properties = []
        self.handlers = {}
    
        