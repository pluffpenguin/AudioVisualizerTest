import numpy as np
import matplotlib.pyplot as plt


class WaveformPlot:
    def __init__(self, SAMPLE_RATE, LENGTH, AMP_CONSTANT) -> None:
        self.SAMPLE_RATE = SAMPLE_RATE
        self.LENGTH = LENGTH
        self.AMP_CONSTANT = AMP_CONSTANT
        
        self.fig = None
        self.ax = None
        self.line = None

    def setup_fig(self):
        self.fig, self.ax = plt.subplots()

        self.ax.set_ylim(-self.AMP_CONSTANT, self.AMP_CONSTANT)
        self.ax.set_xlim(0, self.LENGTH)

        self.ax.set_ylabel('Amplitude')
        self.ax.set_xlabel('Chunk')

        x = np.arange(0, 2 * self.LENGTH, 2)
        self.line, = self.ax.plot(x, np.random.rand(self.LENGTH), 'r')
        self.line.set_color('blue')

        self.fig.show()

    def draw(self, data_output):
        self.line.set_ydata(data_output)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
