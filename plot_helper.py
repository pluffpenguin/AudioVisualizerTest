import numpy as np
import matplotlib as plt

def line_func(t, r_init, v_slope):
    point = r_init + t*v_slope
    return point

class PlotHelper:
    def __init__(self, ax: plt.axes, tbound, column_count):
        self.ax = ax
        self.tbound = tbound
        self.column_count = column_count
        
    def plot_line(self, r_init, v_slope, c=None):
        r_init = np.array(r_init)
        v_slope = np.array(v_slope)
        
        x = np.array([])
        y = np.array([])
        z = np.array([])

        for t in range(-self.tbound, self.tbound):
            point = line_func(t, r_init, v_slope)
            x = np.append(x, point[0])
            y = np.append(y, point[1])
            z = np.append(z, point[2])
        
        self.ax.plot3D(x, y, z, c=c)
    
    def plot_point(self, point, c=None, marker=None, s=None):
        self.ax.scatter(point[0], point[1], point[2], c=c, marker=marker, s=s)
        
    def plot_plane(self, starting_point, normal_vector):
        x_axis = np.array([])
        y_axis = np.array([])
        z_axis = np.array([])
        
        # Make x-vector negative, then swap
        inline_xvector_slope = [normal_vector[2], 0, -normal_vector[0]]
        inline_yvector_slope = [0, normal_vector[2], -normal_vector[1]]
        
        for t in range(-self.tbound, self.tbound):
            xline_point = line_func(t, starting_point, inline_xvector_slope)
            yline_point = line_func(t, starting_point, inline_yvector_slope)
            x_axis = np.append(x_axis, xline_point[0])
            y_axis = np.append(y_axis, yline_point[1])
            z_axis = np.append(z_axis, (xline_point[2] + yline_point[2])/2)
            
        x_axis, y_axis = np.meshgrid(x_axis, y_axis)
        z_axis = (x_axis + y_axis)*0
        self.ax.plot_wireframe(x_axis, y_axis, z_axis, color='mediumblue')
        