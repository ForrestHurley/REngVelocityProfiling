import numpy as np
from matplotlib import pyplot as plt

class obstacle(object):
    def __init__(self,x=0,y=0,size=(1,1)):
        self.pos = (x,y)
        if (len(size) == 1):
            self.size = (size,size)
        else:
            self.size = size

    def get_points(self,resolution):
        pass

    def draw(self,color="b"):
        pass

class rectangle(obstacle):
    pass

class ellipse(obstacle):
    pass

class point(obstacle):
    pass

class region(object):
    def __init__(self,size=(10,10)):
        self.size = size
        self.obstacles = [ rectangle(size=size)) ]

    @classmethod
    def RandomBlocks(cls,count=10,area=0.5,size=(10,10))
        pass

    def get_points(self,resolution=1):
        point_sets = []
        for obs in self.obstacles:
            point_sets.append(obs.get_points(resolution=resolution))
        points = np.concatenate(tuple(point_sets)
        return points)
    
    def draw(self,show=False):
        pass 
