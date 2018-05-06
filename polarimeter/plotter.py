import matplotlib.pyplot as plt
from math import sqrt, ceil

class Plotter(object):
    def __init__(self):
        self.plots = []

    def addPlot(self, data, axes, title):
        self.plots.append((data, axes, title))

    def show(self):
        fig = plt.figure()
        count = len(self.plots)
        size = int(ceil(sqrt(count)))
        for i in range(count):
            ax = fig.add_subplot(size, size, i + 1)
            plot = self.plots[i]
            ax.plot(*plot[0])
            plt.axis(plot[1])
            plt.title(plot[2])
        plt.show()
