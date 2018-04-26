import numpy as np
import random
from matplotlib import pyplot as plt

class obstacle(object):
    def __init__(self,x=0,y=0,size=(1,1)):
        self.pos = (x,y)
        if (len(size) > 2):
            pass
            #insert exception here
        if (len(size) == 1):
            self.size = (size,size)
        else:
            self.size = size

    @classmethod
    def RandomObstacle(cls,bottom_left=(0,0),top_right=(10,10),area=None):
        if (area == None):
            max_area = (top_right[0]-bottom_left[0])*(top_right[1]-bottom_left[1])
            area = random.uniform(max_area*0.05,max_area*0.4)

        x_size = random.uniform(0.33333*(area**0.5),3*(area**0.5))
        y_size = area / x_size

        position = (random.uniform(bottom_left[0],top_right[0]-x_size),
                    random.uniform(bottom_left[1],top_right[1]-y_size))
        rand_obs = cls(x=position[0],y=position[1],size=(x_size,y_size))
        return rand_obs

    def get_points(self,resolution):
        return (np.array([self.pos]))

    def contains_point(self,point):
        pass

    def draw(self,color="b",show=False):
        if (show):
            plt.show()

class rectangle(obstacle):
    def get_points(self): 
        x = np.linspace(self.pos[0],self.pos[0]+self.size[0],dtype="int")
        y = np.linspace(self.pos[1],self.pos[1]+self.size[1],dtype="int")
       
        xy = np.concatenate(([x,np.full(x.shape,int(self.pos[1]))], #Don't double count the corners
                        [x,np.full(x.shape,int(self.pos[1]+self.size[1]))],
                        [np.full(y.shape,int(self.pos[0])),y],
                        [np.full(y.shape,int(self.pos[0]+self.size[0])),y]),axis=-1)
        return xy

    def draw(self,color="b",show=False):
        if (show):
            plt.show()

    def contains_points(self,points):
        return np.zeros(points.shape,dtype='bool')

class ellipse(obstacle):
    pass

class list_obstacle(obstacle):
    pass

class cubic_spline(list_obstacle):
    pass

class linear_interpolator(list_obstacle):
    pass

class region(object):
    def __init__(self,size=(10,10)):
        self.size = size
        self.obstacles = [ rectangle(size=size) ] #The region bounding box

    @classmethod
    def RandomBlocks(cls,count=10,total_area=0.3,size=(100,100),safe_points = np.array([])):
        random_region = cls(size)

        uniform_area = size[0]*size[1]*total_area/count
        obstacle_areas = [uniform_area for i in range(count)] #TODO: make code to make sum of areas equal total area

        for area in obstacle_areas:
            while True:
                new_obstacle = rectangle.RandomObstacle(bottom_left=(0,0),
                                 top_right=random_region.size,area=area)
                if not np.any(new_obstacle.contains_points(safe_points)):
                    random_region.obstacles.append(new_obstacle)
                    break
        return (random_region)

    def get_points(self):
        point_sets = []
        for obs in self.obstacles:
            point_sets.append(obs.get_points())
        points = np.concatenate(point_sets,axis=1)
        return (points)
    
    def draw(self,show=True):
        for obs in self.obstacles:
            obs.draw(show=False)
        if (show):
            plt.show()

if __name__ == "__main__":

    from plan_path import path_planner

    planner = path_planner.create_planner()
    planner.plot = True

    area = region.RandomBlocks(2)
    planned_path = planner.generate_path(area)

    plt.plot(planned_path.arc_length)
    plt.show()

    '''
    area = region.RandomBlocks()
    from PythonRobotics.PathPlanning.AStar import a_star
    x, y = area.get_points()
    x = [int(val) for val in x]
    y = [int(val) for val in y]

    #path planning
    sx = 1.
    sy = 1.
    gx = 90.
    gy = 90.

    grid_size = 1.
    robot_size = 1.

    plt.plot(x, y, ".k")
    plt.plot(sx, sy, "xr")
    plt.plot(gx, gy, "xb")
    plt.grid(True)
    plt.axis("equal")

    rx, ry = a_star.a_star_planning(sx, sy, gx, gy, x, y, grid_size, robot_size)
    
    plt.plot(rx, ry, "-r")
    plt.show()
    '''
