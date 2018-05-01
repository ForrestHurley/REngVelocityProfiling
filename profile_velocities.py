import numpy as np
from matplotlib import pyplot as plt
from scipy import interpolate
from path import path

class profile(object):
    def __init__(self,path,constraint = None):
        self.path = path
        if constraint = None:
            self.velocities = np.full(shape = (path.resolution), fill_value = np.inf)
        else:
            self.velocities = constraint.get_max_velocity(path.t_values)

    def _nullify_properties(self):
        self._total_time = None
        self._max_velocity = None
        self._max_acceleration = None
        self._max_nth_derivative = None

    @property
    def total_time(self):
        if (self._total_time is None):
            pass
        return self._total_time 

    @property
    def max_velocity(self):
        pass

    @property
    def max_acceleration(self):
        pass

    def max_nth_derivative(self,n):
        pass

class vel_profiler(object):
    def __init__(self):
        pass

    def generate_velocities(self, constraints):
        pass

class max_vel_profiler(vel_profiler):
    pass

class trapezoidal_profiler(vel_profiler):
    pass

if __name__ == "__main__":
    from plan_path import path_planner
    import generate_regions

    planner = path_planner.create_planner()
    planner.plot = True

    area = generate_regions.region.RandomBlocks(20)
    planned_path = planner.generate_path(area)

    
