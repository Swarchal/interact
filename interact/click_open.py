from utils import open_equalize
import numpy as np
import matplotlib.pyplot as plt

def click_merge(event, data, x_col, y_col, col_list, title=None,
                fudge_factor = 0.025):
    """
    Click on point in matplotlib figure, create a merged RGB image associated
    with that point.

    Parameters:
    ------------
    event : click
    data : pandas DataFrame
    x_col : string
        column relating to x-coord
    y_col : string
        column relating to y-coord
    col_list : list of strings
        list of column names for red, blue, green channel
    title : string
        column name for image title
    fudge_factor : float
        how close to a point to trigger as a click
    """
    ix, iy = event.xdata, event.ydata
    print("INFO: clicked at ({0:5.2f}, {1:5.2f})".format(ix, iy))
    ax = plt.gca()
    dx = fudge_factor * (ax.get_xlim()[1] - ax.get_xlim()[0])
    dy = fudge_factor * (ax.get_ylim()[1] - ax.get_ylim()[0])
    x = data[x_col]
    y = data[y_col]
    colours_data = [data[col] for col in col_list]
    for i in range(len(x)):
        if (x[i] > ix-dx and x[i] < ix+dx and y[i] > iy-dy and y[i] < iy+dy):
            print("INFO: close to point ({0:5.2f}, {1:5.2f})".format(x[i], y[i]))
            rgb_list = [open_equalize(col[i]) for col in colours_data]
            rgb = np.dstack(rgb_list)
            plt.figure()
            plt.imshow(rgb)
            if title is not None:
                img_title = df[title][i]
                plt.title(img_title)
            plt.axis("off")
            plt.show()
            break



def click_single(event, data, x_col, y_col, img_tag):
    """
    trigger event when click close to a point in a matplotlib figure

    Parameters:
    ------------
    event : click
    data : pandas DataFrame
    x_col : string
        column relating to x-coord
    y_col : string
        column relating to y-coord
    img_tab : string
        column listing image URLs
    """

    ix, iy = event.xdata, event.ydata
    print("clicked at x={0:5.2f}, y={1:5.2f}".format(ix, iy))
    ax = plt.gca()
    dx = 0.025 * (ax.get_xlim()[1] - ax.get_xlim()[0])
    dy = 0.025 * (ax.get_ylim()[1] - ax.get_ylim()[0])
    x = data[x_col]
    y = data[y_col]
    images = data[img_tag].values.tolist()
    for i in range(len(x)):
        if (x[i] > ix-dx and x[i] < ix+dx and y[i] > iy-dy and y[i] < iy+dy):
            print("opening {}".format(images[i]))
            img_array = open_equalize(images[i])
            plt.figure()
            plt.imshow(img_array, cmap=plt.cm.Greys_r)
            plt.show()
            break


def click_locate(event):
    """
    Test function that returns location of click on a graph, and the closest
    point to that click location.
    """

    ix, iy = event.xdata, event.ydata
    print("clicked at x={0:5.2f}, y={1:5.2f}".format(ix, iy))
    ax = plt.gca()
    dx = 0.025 * (ax.get_xlim()[1] - ax.get_xlim()[0])
    dy = 0.025 * (ax.get_ylim()[1] - ax.get_ylim()[0])
    for i in range(len(x)):
        if (x[i] > ix-dx and x[i] < ix+dx and y[i] > iy-dy and y[i] < iy+dy):
            print(i)
            print("clicked close to point {}, {}".format(x[i], y[i]))
