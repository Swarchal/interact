from interact.utils import open_equalize
from collections import namedtuple
import numpy as np
import matplotlib.pyplot as plt


def click_merge(event, data, x_col, y_col, channels, title=None,
                fudge_factor=0.025, verbose=True):
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
    title : string (default=None)
        column name for image title, e.g compound name
    fudge_factor : float (default=0.025)
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
        _plot_ch_lists(ix, iy, dx, dy, channels, data, x, y, title, verbose)
    if isinstance(channels, dict):
        # if channels are stored in a dictionary, then need to create an RGB
        # image with the correct colours for each channel column
        # raise NotImplementedError("not made this yet!")
        _plot_ch_dict(ix, iy, dx, dy, channels, data, x, y, title, verbose)


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


def _check_ch_dict(channels):
    if len(channels) > 3:
        raise ValueError("Expected upto 3 channels got %d" % len(channels))
    if not all(i in ["red", "green", "blue"] for i in channels.keys()):
        raise ValueError("Unexpected channel name")


def _plot_ch_lists(ix, iy, dx, dy, channels, data, x, y, title, verbose):
    file_names = [data[col] for col in channels]
    for i in range(len(x)):
        if (x[i] > ix-dx and x[i] < ix+dx and y[i] > iy-dy and y[i] < iy+dy):
            if verbose:
                print("INFO: close to point ({0:5.2f}, {1:5.2f})"\
                      .format(x[i], y[i]))
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
def _plot_ch_dict(ix, iy, dx, dy, channels, data, x, y, title, verbose):
    """
    plot RGB image from dictionary of channels.
    Channels can be any or all of [red, green, blue], with the dict keys
    specifying the colour of the image.
    """
    _check_ch_dict(channels)
    # create dictionary relating channel name to RGB slice
    channel_slice = {"red":0, "green":1, "blue":2}
    # create dictionary of file paths, list of each channel
    img_dict = _create_image_dict(channels, data)
    for i in range(len(x)):
        if (x[i] > ix-dx and x[i] < ix+dx and y[i] > iy-dy and y[i] < iy+dy):
            if verbose:
                print("INFO: close to point ({0:5.2f}, {1:5.2f})"\
                      .format(x[i], y[i]))

            ###################################################################
            # TODO get image lists, need to keep track of which channel
            ###################################################################
            ## does this need to be done with a dictionary??
            ## could be done instead with a data frame and extract column names
            ## rather than use a dictionary
            #------------------------------------------------------------------
            # get index of point matching click
            # look up index in dictionary in associated channels
            # create dictionary of single image
            # use dict keys to specify channel slice in RGB array
            # look up key in channel_slice dict to get slice number
            # insert image into slice

            # get x,y limits from image
            y_dim, x_dim = images[0].shape
            # create an RGB array of all zeros
            rgb_array = np.zeros((3, y_dim, x_dim), dtype=np.uint8)
            # plot array as an RGB image
            plt.figure()
            plt.imshow(rgb_array)
            if title is not None:
                img_title = df[title][i]
                plt.title(img_title)
            plt.axis("off")
            plt.show()
            break


def _create_image_dict(channels, data):
    """create dictionary of lists, one list per channel"""
    img_dict = dict()
    for ch, col in channels.items():
        img_dict[ch] = data[col]
    return img_dict