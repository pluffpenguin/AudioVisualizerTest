import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.animation import FuncAnimation

AMP_CONSTANT = 6000

class AnalysisPlot:
    def __init__(self, DISPLAY_AMP) -> None:
        self.fig = plt.figure()
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.labels = ['Max', 'Avg']
        self.data = [0, 0]
        self.ax.bar(self.labels, self.data)
        self.DISPLAY_AMP = DISPLAY_AMP
        if self.DISPLAY_AMP:
            plt.ylim(top=1000)
            plt.show(block=False)
        
    def get_fig(self):
        return self.fig
    
    def get_max_amp(self, array):
        self.data[0] = np.amax(array)
        return self.data[0]

    def get_flat_average(self, array):
        self.data[1] = np.average(np.abs(array))
        return self.data[1]
    
    def animate(self):
        print()
    
    def plot_bar(self):
        if self.DISPLAY_AMP: 
            plt.cla()
            plt.ylim(AMP_CONSTANT)
            self.ax.bar(self.labels, self.data)
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()
        
        