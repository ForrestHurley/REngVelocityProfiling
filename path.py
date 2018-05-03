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
        self._t_values = None

    def draw_path(self):
        plt.plot(self.raw_points[0],self.raw_points[1])
        plt.show()

    def draw_curvature(self):
        plt.plot(np.abs(self.curvature(self.t_values)))
        plt.show()

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
    def t_values(self):
        if (self._t_values is None):
            self._t_values = np.linspace(0,self.raw_points.shape[1],self.resolution)
        return self._t_values

    @property
    def raw_interp_points(self):
        if (self._raw_interp_points is None):
            self._raw_interp_points = self.point_interpolator(self.t_values)
            
        return self._raw_interp_points

    @property
    def arc_length(self):
        if (self._arc_length is None):
            distances = np.sum(np.diff(self.raw_interp_points,n=1,axis=-1)**2,axis=0)**0.5

            out = np.empty(self.raw_interp_points.shape[1], dtype = 'double')
            np.cumsum(distances, out = out[1:])
            out[0] = 0

            self._arc_length = out        

        return self._arc_length

    @property
    def uniform_points(self):
        if (self._uniform_points is None):
            self._uniform_points = interpolate.make_interp_spline(self.arc_length,self.t_values) 
        return self._uniform_points

    @property
    def curvature(self):
        if (self._curvature is None):
            first_deriv = self.point_interpolator.derivative(nu=1)(self.t_values)
            second_deriv = self.point_interpolator.derivative(nu=2)(self.t_values)

            numerator = first_deriv[0]*second_deriv[1] - first_deriv[1]*second_deriv[0]
            denominator = (first_deriv[0]**2 + first_deriv[1]**2)**(3./2.)

            self._curvature = interpolate.make_interp_spline(self.t_values, numerator / denominator)
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

    def iterate_path(self,forward = True):
        return path_iterator(self,forward)

    def __iter__(self):
        return path_iterator(self)

class path_iterator(object):
    def __init__(self,path,forward = True,step = None):
        self.resolution = path.resolution
        self.path = path
        self.forward = forward
        if (step is None):
            self.step = (forward * 2 - 1) * path.length / path.resolution
        else:
            self.step = step
            forward = step > 0
        if forward:
            self.current = 0
        else:
            self.current = path.length

    def __iter__(self):
        return self

    def next(self):
        if self.forward:
            if self.current > self.path.length:
                raise StopIteration
        else:
            if self.current < 0:
                raise StopIteration
        self.current += self.step
        spline_parameter = self.path.uniform_points(self.current)
        location = self.path.raw_interpolator(spline_parameter)
        curvature = self.path.curvature(spline_parameter)

        #current arclength, distance, spline parameter, x y location, curvature from interpolator
        return self.current, self.step, spline_parameter, location, curvature

