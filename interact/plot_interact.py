from interact import click_open
import matplotlib.pyplot as plt
import pandas as pd


def plot_interactive(data, x, y, col_list, **kwargs):
    """
    docstring
    """
    plt.close("all")
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(data[x], data[y], **kwargs)
    ax.grid()
    fig.canvas.mpl_connect("button_press_event",
                           lambda event:
                           click_open.click_merge(
                               event, data, x, y, col_list))
    plt.show()
