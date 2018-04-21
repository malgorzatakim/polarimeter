import matplotlib.pyplot as plt
from math import sqrt, ceil

class Plotter(object):
    def __init__(self):
        self.plots = []

    def addPlot(data, title):
        plots.append((data, title))

    def show():
        plt.figure()
        count = len(plots)
        size = int(ceil(sqrt(count))
        for i in range(count):
            ax = fig.add_subplot(size, size, i + 1)
            plot = plots[i]
            ax.plot(*plot[0])
            plt.title(plot[1])
        plt.show()