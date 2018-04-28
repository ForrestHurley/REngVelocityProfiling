import numpy as np
from scipy import interpolate

class constraint(object):
    def __init__(self):
        self.interp_degree_list = [[]]
        self.initials = []
        self.finals = []
        self.bounds = [-np.inf,np.inf]

    @classmethod
    def minimal_constraint(cls,initial_vel=0,final_vel=0,max_vel=10,bounds = (0,10)):
        minimal = cls()
        minimal.set_start_constraint(initial_vel)
        minimal.set_end_constraint(final_vel)
        minimal.add_interp_constraint(0,max_vel,extrapolate=True)
        minimal.set_bounds(*bounds)
        return minimal

    def set_bounds(self,min_bound = -np.inf, max_bound = np.inf):
        self.bounds = [min_bound,max_bound]

    def add_interp_constraint(self,x,y,n=1,extrapolate=False,degree=3):
        if extrapolate:
            fill = (y[0],y[-1])
        else:
            fill = np.inf

        new_interp = interpolate.interp1d(
                        x = x, y = y,
                        kind = 'cubic', bounds_error = False,
                        fill_value = fill)

        if n > len(self.interp_degree_list):
            self.interp_degree_list += [[]*(n-len(self.interp_degree_list))]

        self.interp_degree_list[n-1].append(new_interp)

    def set_end_constraint(self,y,n=1):
        if n > len(self.initials):
            self.initials += [0.]*(n-len(self.interp_degree_list))
       
        self.initials[n-1] = y 

    def set_start_constraint(self, y, n = 1):
        if n > len(self.finals):
            self.finals += [0.]*(n-len(self.interp_degree_list))
       
        self.finals[n-1] = y 

    def get_mins(self,points):
        mins = np.zeros(len(self.interp_degree_list),points.shape[0])

        for i in range(len(self.interp_degree_list)):
            mins[i] = self.get_min_nth(points,n = i + 1)

        return mins

    def get_min_nth(self,points,n=1):
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

    def get_min_velocity(self,points):
        return self.get_min_nth(points,n=1)

