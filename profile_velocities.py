import numpy as np
from matplotlib import pyplot as plt
from scipy import Interpolate

class path(object):
    def __init__(self,points,resolution=1000):
        self._raw_points = points
        self._resolution = resolution
       
        self._nullify_properties()
 
    def _nullify_properties(self):
        self._arc_length = None
        self._uniform_points = None
        self._curvature = None
        self._t_hat = None
        self._n_hat = None

    @property
    def raw_points(self):
        pass

    @raw_points.setter
    def raw_points(self,points):
        self._nullify_properties()
        pass

    @property
    def resolution(self):
        pass

    @resolution.setter
    def resolution(self):
        self._nullify_properties()
        pass

    @property
    def arc_length(self):
        if (_arc_length == None):
        
        else:
            return _arc_length

    @property
    def uniform_points(self):
        if (_uniform_points == None):
        
        else:
            return _uniform_points

    @property
    def curvature(self):
        if (_curvature == None):
        
        else:
            return _curvature

    @property
    def t_hat(self):
        if (_t_hat == None):
        
        else:
            return _t_hat

    @property
    def n_hat(self):
        if (_n_hat == None):
        
        else:
            return _n_hat

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
