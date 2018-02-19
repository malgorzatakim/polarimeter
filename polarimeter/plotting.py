import numpy as np
import matplotlib.pyplot as plt

def plot(time, obj, ref, titles):
    a = 221
    fig = plt.figure()
    for i in range((len(obj) - 1)):
        fig.add_subplot(a + i)
        plot(time, np.real(ref[i]), time, np.real(obj[i]))
        plt.title(title[i])
    plt.show()