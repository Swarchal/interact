from utils import open_equalize
from collections import namedtuple
import numpy as np
import matplotlib.pyplot as plt


def click_merge(event, data, x_col, y_col, channels, title=None,
                fudge_factor=0.025):
    """
    Click on point in matplotlib figure, create a merged RGB image associated
    with that point.

    Parameters:
    ------------
    event : click
    data : pandas DataFrame
    x_col : string
        column relating to x-coordinate
    y_col : string
        column relating to y-coordinate
    channels: list or dict
        list of column names for red, blue, green channel, or dictionary of upto
        three channels with associated channels named (red, green or blue)
    title : string
        column name for image title, e.g compound name
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
    if isinstance(channels, list):
        # if channels in list the pass colours in order (red, green, blue)
        _plot_channels_lists(ix, iy, dx, dy, channels, data, x, y, title)
    if isinstance(channels, dict):
        # if channels are stored in a dictionary, then need to create an RGB
        # image with the correct colours for each channel column
        raise NotImplementedError("not made this yet!")
        _plot_channels_dict(ix, iy, dx, dy, channels, data, x, y, title)


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


def _check_channels_dict(channels):
    if len(channels) > 3:
        raise ValueError("Expected upto 3 channels got %d" % len(channels))
    if not all(i in ["red", "green", "blue"] for i in channels.keys()):
        raise ValueError("Unexpected channel name")


def _plot_channels_lists(ix, iy, dx, dy, channels, data, x, y, title):
    file_names = [data[col] for col in channels]
    for i in range(len(x)):
        if (x[i] > ix-dx and x[i] < ix+dx and y[i] > iy-dy and y[i] < iy+dy):
            print("INFO: close to point ({0:5.2f}, {1:5.2f})".format(x[i], y[i]))
            rgb_list = [open_equalize(col[i]) for col in file_names]
            rgb = np.dstack(rgb_list)
            plt.figure()
            plt.imshow(rgb)
            if title is not None:
                img_title = df[title][i]
                plt.title(img_title)
            plt.axis("off")
            plt.show()
            break


# TODO
def _plot_channels_dict(ix, iy, dx, dy, channels, data, x, y, title):
    _check_channels_dict(channels)
    # create dictionary relating channel name to RGB slice
    channel_slice = {"red":0, "green":1, "blue":2}
    # create dictionary of file paths, list of each channel
    img_dict = _create_image_dict(channels, data)
    for i in range(len(x)):
        if (x[i] > ix-dx and x[i] < ix+dx and y[i] > iy-dy and y[i] < iy+dy):
            print("INFO: close to point ({0:5.2f}, {1:5.2f})".format(x[i], y[i]))

            # TODO get image lists, need to keep track of which channel
            # use a dictionary? - iterate through values from all keys?

            # get x,y limits from image to create empty 3D array
            y_dim, x_dim = images[0].shape[:2]
            rgb_array = np.zeros((3, y_dim, x_dim), dtype=np.uint8)

            plt.figure()
            plt.imshow(rgb_array)
            if title is not None:
                img_title = df[title][i]
                plt.title(img_title)
            plt.axis("off")
            plt.show()
            break


def _create_image_dict(channels, data):
    """ create dictionary of lists, one list per channel """
    img_dict = dict()
    for ch, col in channels.items():
        img_dict[ch] = data[col]
    return img_dict