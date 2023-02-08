import numpy as np
import matplotlib.pyplot as plt
from plot_helper import PlotHelper

axis_bound = 50
column_count = 5 # Used to control the amount of squares on length of mesh

x_axis = np.linspace(-axis_bound, axis_bound, column_count)
y_axis = np.linspace(-axis_bound, axis_bound, column_count)
z_axis = np.linspace(-axis_bound, axis_bound, column_count)

print(x_axis, 'befpore;')

x_axis, y_axis = np.meshgrid(x_axis, y_axis)

print(x_axis, 'after')

eq = x_axis*0 + y_axis*0

# Setup ax
ax = plt.axes(projection='3d')
ax.set_xlabel("X Axis")
ax.set_ylabel("Y Axis")
ax.set_zlabel("Z Axis")
ax.set_title("Line Equation")
ax.set_axis_on()

# ax2 = plt.gca() # Make sure it does not override the previous plot
# ax.plot_wireframe(x_axis, y_axis, eq, color='mediumblue')

plotHelper = PlotHelper(ax, 10, 5)

# ax.plot3D(x, y, z)
# plotHelper.plot_point([1, 0, 0], c='green', marker='o', s=5)
# plotHelper.plot_point([0, 1, 0], c='green', marker='o', s=5)
# plotHelper.plot_point([0, 0, 1], c='green', marker='o', s=5)

# plotHelper.plot_line([0, 1, 0], [0, 1, -1], c='blue')
# plotHelper.plot_line([0, 0, 1], [-1, 0, 1], c='blue')
# plotHelper.plot_line([1, 0, 0], [-1, 1, 0], c='blue')
plotHelper.plot_line([0, 0, 0], [3, 1, 8], c='fuchsia')
plotHelper.plot_line([0, 0, 0], [8, 0, -3], c='chartreuse')
plotHelper.plot_line([0, 0, 0], [0, 8, -1], c='dodgerblue')

plotHelper.plot_plane([0, 0, 0], [3, 1, 8])

plt.show()
