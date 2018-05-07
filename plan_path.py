from matplotlib import pyplot as plt
from path import path

class path_planner(object):
    def __init__(self,verbose=False,planner=None,start=(10.,10.),goal=(90.,90.),plot=True):
        if planner == None:
            planner = self.AStar
        self.planner = planner
        self.start = start
        self.goal = goal          
        self.plot = plot
        self.verbose = verbose
 
    @classmethod
    def create_planner(cls,planner="AStar"):
        try:
            planner_func = getattr(cls,planner)
        except AttributeError:
            raise NotImplementedError("path_planner does not implement `{}`".format(method_name))
        return cls(planner_func)

    def AStar(self):
        from PythonRobotics.PathPlanning.AStar import a_star
        a_star.show_animation = self.plot
        return a_star.a_star_planning

    def generate_path(self,region):
        points = self.make_plan(region)

        if len(points[0]) > 0:
            planned_path = path(points)
            return planned_path
        else:
            return None

    def make_plan(self,region):
        x, y = region.get_points()
        x = [int(val) for val in x]
        y = [int(val) for val in y]

        grid_size = 1.
        robot_size = 1.

        #show_animation = self.plot #The imported libraries use global variables

        if (self.plot):
            region.draw(show = False)
            plt.plot(self.start[0],self.start[1],"xr")
            plt.plot(self.goal[0],self.goal[1],"xb")
            plt.grid(True)
            plt.axis("equal")

        try:
            rx, ry = self.planner()(self.start[0], 
                                    self.start[1], 
                                    self.goal[0], 
                                    self.goal[1], 
                                    x, y, 
                                    grid_size,
                                    robot_size)
        except ValueError as e:
            if self.verbose:
                print("Planning failed: " + str(e))
            return [], []

        if (self.plot):
            plt.plot(rx, ry, "-r")
            plt.show()

        return rx, ry  
