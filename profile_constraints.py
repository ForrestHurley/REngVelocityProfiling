import numpy as np
from scipy import interpolate

class constraint(object):
    def __init__(self):
        self.interp_degree_list = [[]]
        self.initials = []
        self.finals = []
        self.bounds = [0,10]
        self.iter_resolution = 100

    @classmethod
    def minimal_constraint(cls,initial_vel=0,final_vel=0,max_vel=10,bounds = (0,10)):
        minimal = cls()
        minimal.set_start_constraint(initial_vel)
        minimal.set_end_constraint(final_vel)
        minimal.add_interp_constraint(np.array([0,max_vel]),extrapolate=True)
        minimal.set_bounds(*bounds)
        return minimal

    def path_2d_acceleration(cls,path,initial_vel=0,final_vel=0,max_vel=10,max_acc=10):
        pass

    def set_bounds(self,min_bound = -np.inf, max_bound = np.inf):
        self.bounds = [min_bound,max_bound]

    def add_interp_constraint(self, vals, n = 1, extrapolate = False):
        if extrapolate:
            fill = (vals[1,0],y[1,-1])
        else:
            fill = np.inf

        new_interp = interpolate.interp1d(
                        x = vals[1], y = vals[0],
                        kind = 'cubic', bounds_error = False,
                        fill_value = fill)

        if n > len(self.interp_degree_list):
            self.interp_degree_list += [[]*(n-len(self.interp_degree_list))]

        self.interp_degree_list[n-1].append(new_interp)
    
    def overwrite_interp_constraint(self, vals, n = 1, extrapolate = False):
        pass

    def overwrite_lowest_constraints(self, vals, extrapolate = False):
        pass

    def set_start_constraint(self,y,n=1):
        if n > len(self.initials):
            self.initials += [0.]*(n-len(self.initials))
       
        self.initials[n-1] = y 

    def set_end_constraint(self, y, n = 1):
        if n > len(self.finals):
            self.finals += [0.]*(n-len(self.finals))
       
        self.finals[n-1] = y 

    def get_maxs(self,points):
        maxs = np.zeros(len(self.interp_degree_list),points.shape[0])

        for i in range(len(self.interp_degree_list)):
            maxs[i] = self.get_max_nth(points,n = i + 1)

        return maxs

    def get_max_nth(self,points,n=1):
        degree = self.interp_degree_list[n-1]
        tmp_vals = np.zeros(len(degree),points.shape[0])

        for constraint, i in zip(degree,range(len(degree))):
            tmp_vals[i] = constraint(points)

        raw_min = np.nanmin(tmp_vals,axis=1)
       
        if len(self.initials) >= n: 
            raw_min[points <= self.bounds[0]] = self.initials[n-1]
        if len(self.finals) >= n:
            raw_min[points >= self.bounds[1]] = self.finals[n-1]

        return raw_min

    def get_max_velocity(self,points):
        return self.get_max_nth(points,n=1)

    def __iter__(self):
        return get_as_array(self)

    def get_as_array(self,point_count = None):
        if point_count is None:
            point_count = self.iter_resolution
        points = np.linspace(self.bounds[0],self.bounds[1],point_count)
        return self.get_maxs(points)

    def apply_iterative_func(self,foo,point_count = None,forward = True, history_size = 1):
        if point_count is None:
            point_count = self.iter_resolution

        val_array = self.get_as_array(point_count)
        if forward:
            val_array = np.fliplr(val_array)

        new_vals = np.full(val_array.shape,np.inf)
        for i in range(history_size, val_array):
            pass
       
        self.overwrite_lowest_constraints(new_vals, extrapolate = True) 
