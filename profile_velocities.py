import numpy as np
from matplotlib import pyplot as plt
from scipy import interpolate
from path import path
from profile_constraints import constraint

class profile(object):
    def __init__(self,constraint):
        self.points = constraint.get_points()
        self.velocities = constraint.get_max_velocity(points = self.points)

        self._nullify_properties()        

    def _nullify_properties(self):
        self._times = None
        self._total_time = None
        self._max_velocity = None
        self._max_acceleration = None
        self._max_nth_derivative = None

    @property
    def times(self):
        if self._times is None:
            diff_xs = np.diff(self.points)
            mean_vels = (self.velocities[:-1] + self.velocities[1:]) / 2

            delta_ts =  diff_xs / mean_vels

            out = np.empty(self.velocities.shape[0], dtype = 'double')
            np.cumsum(delta_ts, out = out[1:])
            out[0] = 0

            self._times = out
        return self._times

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
        constraints.apply_iterative_func(self.velocity_func, forward = True)
        constraints.apply_iterative_func(self.velocity_func, forward = False)

        return constraints

    def velocity_func(self):
        pass

class trapezoidal_profiler(vel_profiler):
    def __init__(self, max_acceleration = 5):
        super().__init__()
        self.max_acc = max_acceleration

    def velocity_func(self,delta_location,velocities):
        square = velocities ** 2
        delta_square = 2 * self.max_acc * delta_location    
    
        return (square + delta_square) ** 0.5

if __name__ == "__main__":
    #from plan_path import path_planner
    #import generate_regions

    #planner = path_planner.create_planner()
    #planner.plot = True

    #area = generate_regions.region.RandomBlocks(20)
    #planned_path = planner.generate_path(area)
    from path import path
    parameter = np.linspace(0,5,100)
    planned_path = path([parameter**2,10*np.sin(parameter)])
    planned_path.draw_path()
    planned_path.draw_curvature()

    path_constraint = constraint.from_2d_path(path = planned_path, max_acc = 1, max_vel = 6, resolution = 1000)

    profiler = trapezoidal_profiler(max_acceleration = 10)
    new_constraint = profiler.generate_velocities(path_constraint)
    
    vel_profile = profile(new_constraint)

    print("Profile generated")
    plt.plot(vel_profile.times, vel_profile.velocities)
    plt.show()
