import numpy as np
from scipy import interpolate
from inspect import signature

class constraint(object):
    def __init__(self,bounds = (0, 10), resolution = 100):
        self.interp_degree_list = [[]]
        self.initials = []
        self.finals = []
        self.bounds = list(bounds)
        self.iter_resolution = resolution

    @classmethod
    def minimal_constraint(cls,initial_vel=0,final_vel=0,max_vel=10,bounds = (0,10), resolution = 100):
        minimal = cls(bounds = bounds, resolution = resolution)
        minimal.set_start_constraint(initial_vel)
        minimal.set_end_constraint(final_vel)
        minimal.add_interp_constraint(np.array([[0],[max_vel]]),extrapolate=True)
        return minimal

    @classmethod
    def from_2d_path(cls, path, 
                    initial_vel = 0, 
                    final_vel = 0, 
                    max_vel = 10, 
                    max_acc = 5, 
                    resolution = 100):
        minimal = cls.minimal_constraint(initial_vel = initial_vel, 
                                        final_vel = final_vel,
                                        max_vel = max_vel,
                                        bounds = (path.arc_length[0], path.arc_length[-1]),
                                        resolution = resolution)

        points = minimal.get_points()
        limited_vel = np.sqrt(max_acc / np.abs(path.curvature(path.uniform_points(points))))

        minimal.add_interp_constraint(np.array([points,limited_vel]),extrapolate = False)

        return minimal

    def set_bounds(self,min_bound = 0, max_bound = 10):
        self.bounds = [min_bound,max_bound]

    def add_interp_constraint(self, vals, n = 1, extrapolate = False):
        if extrapolate:
            fill = (vals[1,0],vals[1,-1])
        else:
            fill = np.inf

        if vals.shape[1] == 0:
            raise ValueError("No points to interpolate")
        elif vals.shape[1] == 1:
            kind = 'zero'
        elif vals.shape[1] == 2:
            kind = 'linear'
        elif vals.shape[1] == 3:
            kind = 'quadratic'
        else:
            kind = 'cubic'

        new_interp = interpolate.interp1d(
                        x = vals[0], y = vals[1],
                        kind = kind, bounds_error = False,
                        fill_value = fill)

        if n > len(self.interp_degree_list):
            self.interp_degree_list += [[]*(n-len(self.interp_degree_list))]

        self.interp_degree_list[n-1].append(new_interp)
    
    def overwrite_interp_constraint(self, vals, n = 1, extrapolate = False):
        if n > len(self.interp_degree_list):
            self.interp_degree_list += [[]*(n-len(self.interp_degree_list))]
        else:
            self.interp_degree_list[n-1] = []
        self.add_interp_constraint(vals,n,extrapolate)

    def overwrite_lowest_constraints(self, points, vals, extrapolate = False):
        for iter_vals, n in zip(vals,range(1,vals.shape[0]+1)):
            self.overwrite_interp_constraint(np.array([points,iter_vals]), n, extrapolate)

    def add_lowest_constraints(self, points, vals, extrapolate = False):
        for iter_vals, n in zip(vals, range(1, vals.shape[0] + 1)):
            self.add_interp_constraint(np.array([points,iter_vals]), n, extrapolate)

    def set_start_constraint(self,y,n=1):
        if n > len(self.initials):
            self.initials += [0.]*(n-len(self.initials))
       
        self.initials[n-1] = y 

    def set_end_constraint(self, y, n = 1):
        if n > len(self.finals):
            self.finals += [0.]*(n-len(self.finals))
       
        self.finals[n-1] = y 

    def get_maxs(self,points):
        maxs = np.zeros((len(self.interp_degree_list),points.shape[0]))

        for i in range(len(self.interp_degree_list)):
            maxs[i] = self.get_max_nth(points,n = i + 1)

        return maxs

    def get_max_nth(self,points,n=1):
        degree = self.interp_degree_list[n-1]
        tmp_vals = np.zeros((len(degree),points.shape[0]))

        for constraint, i in zip(degree,range(len(degree))):
            tmp_vals[i] = constraint(points)

        raw_min = np.nanmin(tmp_vals,axis=0)
      
        if len(self.initials) >= n: 
            raw_min[points <= self.bounds[0]] = self.initials[n-1]
        if len(self.finals) >= n:
            raw_min[points >= self.bounds[1]] = self.finals[n-1]

        return raw_min

    def get_max_velocity(self,points = None):
        if points is None:
            points = self.get_points()
        return self.get_max_nth(points,n=1)

    def __iter__(self):
        return get_as_array(self)

    def get_points(self, point_count = None):
        if point_count is None:
            point_count = self.iter_resolution
        epsilon = 1e-5
        points = np.linspace(self.bounds[0] - epsilon,
                            self.bounds[1] + epsilon,
                            point_count)
        return points

    def get_as_array(self,point_count = None, points = None):
        if points is None:
            points = self.get_points(point_count)
        return self.get_maxs(points)

    def apply_iterative_func(self,foo,point_count = None,forward = True, history_size = 1):
        if point_count is None:
            point_count = self.iter_resolution

        val_array = self.get_as_array(point_count)
        points = self.get_points(point_count)
        loc_array = np.diff(points)
        if forward:
            val_array = np.fliplr(val_array)

        foo_sig = signature(foo)
        parameter_count = len(foo_sig.parameters) - 1

        for i, location in zip(range(history_size, val_array.shape[1]),loc_array[(history_size - 1):]):
            val_array[:parameter_count, i] = np.minimum(val_array[:parameter_count, i],
                            foo(location,*val_array[:parameter_count,(i - history_size):i]))

        if forward:
            val_array = np.fliplr(val_array)

        self.add_lowest_constraints(points,val_array[:parameter_count], extrapolate = True) 

