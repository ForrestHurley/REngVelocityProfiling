
class constraint(object):
    def __init__(self):
        pass

    def get_maxes(self,object_state=None):
        pass

    def get_max_nth(self,object_state=None,n=1):
        pass

class constant_constraint(constraint):
    def __init__(self,maximum_kinematics):
        self.maxes = maximum_kinematics

    def get_maxes(self,object_state=None):
        return self.maxes

    def get_max_nth(self,object_state=None,n=1):
        return self.maxes[n]
