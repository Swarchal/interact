from click_open_image_merge import onclick
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def plot_interactive(data, x, y, red, green, blue, **kwargs):
    """
    docstring
    """
    # create plot
    plt.close("all")
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(data[x], data[y], ".")
    ax.grid()

    # create interactive element
    fig.canvas.mpl_connect("button_press_event",
                           lambda event:
                           onclick(event, data, x, y, red, green, blue))
    plt.show()
