import numpy as np
from matplotlib import pyplot as plt
from scipy import interpolate

class path(object):
    def __init__(self,points,resolution=1000):
        self._raw_points = np.array(points)
        self._resolution = resolution
       
        self._nullify_properties()
 
    def _nullify_properties(self):
        self._arc_length = None
        self._point_interpolator = None
        self._raw_interp_points = None
        self._derivatives = None
        self._uniform_points = None
        self._curvature = None
        self._t_hat = None
        self._n_hat = None

    @property
    def raw_points(self):
        return self._raw_points

    @raw_points.setter
    def raw_points(self,points):
        self._nullify_properties()
        self._raw_points = np.array(points)

    @property
    def resolution(self):
        return self._resolution

    @resolution.setter
    def resolution(self,resolution):
        self._nullify_properties()
        self._resolution = resolution

    @property
    def point_interpolator(self):
        if (self._point_interpolator is None):
            self._point_interpolator = interpolate.make_interp_spline(
                                            x = np.arange(self.raw_points.shape[1]),
                                            y = self.raw_points,
                                            axis = 1)
        return self._point_interpolator

    @property
    def raw_interp_points(self):
        if (self._raw_interp_points is None):
            t_values = np.linspace(0,self.raw_points.shape[1],self.resolution)
            self._raw_interp_points = self.point_interpolator(t_values)
            
        return self._raw_interp_points

    @property
    def arc_length(self):
        if (self._arc_length is None):
            distances = np.sum(np.diff(self.raw_interp_points,n=1,axis=-1)**2,axis=0)**0.5

            self._arc_length = np.cumsum(distances)
        
        return self._arc_length

    @property
    def uniform_points(self):
        if (self._uniform_points is None):
            pass 
        return self._uniform_points

    @property
    def curvature(self):
        if (self._curvature is None):
            pass 
        return self._curvature

    @property
    def t_hat(self):
        if (self._t_hat is None):
            pass
        return self._t_hat

    @property
    def n_hat(self):
        if (self._n_hat is None):
            pass
        return self._n_hat

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
