import numpy as np
from matplotlib import pyplot as plt

class profile(object):
    def __init__(self):
        pass

    def total_time(self):
        pass

    def max_velocity(self):
        pass

    def max_acceleration(self):
        pass

    def max_nth_derivative(self,n):
        pass

class vel_profiler(object):
    def __init__(self):
        pass

    def generate_velocities(self, points):
        pass

class linear_profiler(vel_profiler):
    pass
   
class linear_trapezoidal_profiler(linear_profiler):
    pass

class linear_s_curve_profiler(linear_profiler):
    pass

class trapezoidal_profiler(vel_profiler):
    pass 
