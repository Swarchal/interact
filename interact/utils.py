"""
utility functions
"""
import random
import numpy as np
from interact import path
from bokeh.plotting import figure, show, output_file, reset_output
from bokeh.layouts import layout
from bokeh.models.layouts import Column
from skimage import io
from skimage import exposure
from skimage import img_as_ubyte


def open_equalize(url, **kwargs):
    """open an image, equalize"""
    return img_as_ubyte(exposure.equalize_adapthist(io.imread(url), **kwargs))


def open_equalize_stack(list_of_urls, **kwargs):
    """open a list of channels and stack into a numpy array"""
    rgb = [open_equalize(url, **kwargs) for url in list_of_urls]
    return np.dstack(rgb)

# TODO how to link the axis to plots that have not been created yet??
# might have to resort to weird object orientated magic
# or if it's possible to access the dw and dh attributes after the object has been
# created could relate all the axes together once all the figures have been created.

def convert_rgb_to_bokeh_rgba(img):
    """
    Convert a normal RGB numpy stack into the stupid bokeh format

    Parameters:
    -----------
    img : np.ndarray
        numpy array with the format (x, y, n_channels, dtype=uint8)

    Returns:
        (x, y, dtype=uint32) numpy array
    """
    bokeh_img = np.dstack([img, 255 * np.ones(img.shape[:2], np.uint8)])
    final_rgba_image = np.squeeze(bokeh_img.view(dtype=np.uint32))
    return final_rgba_image


def convert_grey_to_bokeh_rgba(img):
    """
    Converts normal numpy grayscale image to stupid bokeh format

    Parameters:
    -----------
    img : np.ndarray
        (x, y, dtype=uint8)

    Returns:
    ---------
        (x, y, dtype=uint32) numpy array
    """
    bokeh_img = np.expand_dims(img, img.ndim)
    bokeh_img = np.concatenate([bokeh_img] * 3, axis=-1)
    return convert_rgb_to_bokeh_rgba(bokeh_img)


def create_rgb_figure(paths, width=500, height=500, title=None):
    """
    Create a bokeh rgb figure object from a list of filepaths
    relating to RGB images in that order.

    Parameters:
    ------------
    paths: list of strings
        paths to images in RGB order
    width: int (default=500)
        figure width
    height: int (default=500)
        figure height
    title: string (default=None)
        figure title

    Returns:
    ---------
    bokeh figure object
    """
    assert len(paths) == 3
    img_stack = open_equalize_stack(paths)
    rgb = convert_grey_to_bokeh_rgba(img_stack)
    x_dim, y_dim = rgb.shape[:2]
    fig = figure(width=width, height=height, title=title,
                 x_range=[0, x_dim], y_range=[0, y_dim])
    fig.image_rgba(image=[rgb], x=0, y=0, dw=x_dim, dh=y_dim)
    return fig


def create_bw_figure(path, width=500, height=500, title=None):
    """
    Create a bokeh greyscale figure object from a filepath

    Parameters:
    -----------
    path: string
        path to image
    width: int (default=500)
        figure width
    height: int (default=500)
        figure height
    title: string (default=None)
        figure title

    Returns:
    ---------
    bokeh figure object
    """
    img = open_equalize(path)
    img_bokeh_fmt = convert_grey_to_bokeh_rgba(img)
    x_dim, y_dim = img_bokeh_fmt.shape[:2]
    fig = figure(width=width, height=height, title=title,
                 x_range=[0, x_dim], y_range=[0, y_dim])
    fig.image_rgba(image=[img_bokeh_fmt], x=0, y=0, dw=x_dim, dh=y_dim)
    return fig


def create_rgb_split_figure(paths, title=None):
    """
    docstring

    Returns:
    ---------
    bokeh plot object
    """
    assert len(paths) == 3
    # create images as numpy arrays
    img_stack = open_equalize_stack(paths)
    rgb = convert_rgb_to_bokeh_rgba(img_stack)
    channels = []
    for i in range(3):
        img = convert_grey_to_bokeh_rgba(img_stack[:, :, i])
        channels.append(img)
    # get image dimensions
    x_dim, y_dim = rgb.shape[:2]
    # create figure objects
    p_rgb = figure(width=720, height=700, title=title,
                   x_range=[0, x_dim], y_range=[0, y_dim])
    p_rgb.image_rgba(image=[rgb], x=0, y=0, dw=x_dim, dh=y_dim)
    p_ch1 = figure(width=300, height=250, title=None,
                   x_range=p_rgb.x_range, y_range=p_rgb.y_range)
    p_ch1.image_rgba(image=[channels[0]], x=0, y=0, dw=x_dim, dh=y_dim)
    p_ch2 = figure(width=300, height=250, title=None,
                   x_range=p_rgb.x_range, y_range=p_rgb.y_range)
    p_ch2.image_rgba(image=[channels[1]], x=0, y=0, dw=x_dim, dh=y_dim)
    p_ch3 = figure(width=300, height=250, title=None,
                   x_range=p_rgb.x_range, y_range=p_rgb.y_range)
    p_ch3.image_rgba(image=[channels[2]], x=0, y=0, dw=x_dim, dh=y_dim)
    # separate channels as a column
    column_plots = Column(p_ch1, p_ch2, p_ch3)
    return layout([[p_rgb, column_plots]], sizing_mode="scale_height")


# TODO figure size as a parameter
def create_bw_all_5_figure(paths, title=None):
    """
    docstring

    Returns:
    ---------
    bokeh plot object
    """
    assert len(paths) == 5
    # create images as numpy arrays
    img_stack = open_equalize_stack(paths)
    channels = []
    for i in range(5):
        img = convert_grey_to_bokeh_rgba(img_stack[:, :, i])
        channels.append(img)
    # get image dimensions
    x_dim = y_dim = img_stack[0].shape[0]
    # create figure objects
    p_ch1 = figure(width=420, height=400, title=None,
                   x_range=[0, x_dim], y_range=[0, y_dim])
    p_ch1.image_rgba(image=[channels[0]], x=0, y=0, dw=x_dim, dh=y_dim)
    p_ch2 = figure(width=420, height=400, title=None,
                   x_range=p_ch1.x_range, y_range=p_ch1.y_range)
    p_ch2.image_rgba(image=[channels[1]], x=0, y=0, dw=x_dim, dh=y_dim)
    p_ch3 = figure(width=420, height=400, title=None,
                   x_range=p_ch1.x_range, y_range=p_ch1.y_range)
    p_ch3.image_rgba(image=[channels[2]], x=0, y=0, dw=x_dim, dh=y_dim)
    p_ch4 = figure(width=420, height=400, title=None,
                   x_range=p_ch1.x_range, y_range=p_ch1.y_range)
    p_ch4.image_rgba(image=[channels[3]], x=0, y=0, dw=x_dim, dh=y_dim)
    p_ch5 = figure(width=420, height=400, title=None,
                   x_range=p_ch1.x_range, y_range=p_ch1.y_range)
    p_ch5.image_rgba(image=[channels[4]], x=0, y=0, dw=x_dim, dh=y_dim)
    # separate channels as a column
    column_1 = Column(p_ch1, p_ch2)
    column_2 = Column(p_ch3, p_ch4)
    column_3 = Column(p_ch5)
    return layout([[column_1, column_2, column_3]],
                  sizing_mode="scale_height")


def create_figure(paths, rgb_channels=[5, 4, 1]):
    """
    docstring

    Returns:
    ---------
    bokeh plot object
    """
    assert len(paths) == 5
    # create images as numpy arrays
    img_stack = open_equalize_stack(paths)
    channels = []
    for i in range(5):
        img = convert_grey_to_bokeh_rgba(img_stack[:, :, i])
        channels.append(img)
    # get image dimensions
    x_dim = y_dim = img_stack[0].shape[0]
    # create figure objects
    p_ch1 = figure(width=480, height=450, title=None,
                   x_range=[0, x_dim], y_range=[0, y_dim])
    p_ch1.image_rgba(image=[channels[0]], x=0, y=0, dw=x_dim, dh=y_dim)
    p_ch2 = figure(width=480, height=450, title=None,
                   x_range=p_ch1.x_range, y_range=p_ch1.y_range)
    p_ch2.image_rgba(image=[channels[1]], x=0, y=0, dw=x_dim, dh=y_dim)
    p_ch3 = figure(width=480, height=450, title=None,
                   x_range=p_ch1.x_range, y_range=p_ch1.y_range)
    p_ch3.image_rgba(image=[channels[2]], x=0, y=0, dw=x_dim, dh=y_dim)
    p_ch4 = figure(width=480, height=450, title=None,
                   x_range=p_ch1.x_range, y_range=p_ch1.y_range)
    p_ch4.image_rgba(image=[channels[3]], x=0, y=0, dw=x_dim, dh=y_dim)
    p_ch5 = figure(width=480, height=450, title=None,
                   x_range=p_ch1.x_range, y_range=p_ch1.y_range)
    p_ch5.image_rgba(image=[channels[4]], x=0, y=0, dw=x_dim, dh=y_dim)
    # plot rgb image of channels [5, 3, 1]
    # get rgb channels
    ch_0 = [i-1 for i in rgb_channels]
    rgb_paths = [paths[ch_0[0]], paths[ch_0[1]], paths[ch_0[2]]]
    rgb_stack = open_equalize_stack(rgb_paths)
    rgb = convert_rgb_to_bokeh_rgba(rgb_stack)
    p_rgb = figure(width=480, height=450, title=None,
                   x_range=p_ch1.x_range, y_range=p_ch1.y_range)
    p_rgb.image_rgba(image=[rgb], x=0, y=0, dw=x_dim, dh=y_dim)
    # separate channels as a column
    column_1 = Column(p_ch1, p_ch2)
    column_2 = Column(p_ch3, p_ch4)
    column_3 = Column(p_ch5, p_rgb)
    return layout([[column_1, column_2, column_3]],
                  sizing_mode="scale_height")



def create_rgb_split_plot(paths, title=None, location=None):
    """
    Given a list of paths, this will generate a html plot with an RGB image
    of the paths, and the channels plotted in separate facets

    Parameters:
    -----------
    - paths : list of strings
        image paths
    - title: string (default=None)
    - location: string (default=None)
        Where to save the html output, if None then this will be saved in /tmp

    Returns:
    --------
    Nothing, opens a html page in the web-browser saved at $location
    """
    if location is None:
        # save in /tmp/ with a random name
        random_hash = hex(random.getrandbits(32))
        if title is None:
            location = "/tmp/bokeh_plot_{}.html".format(random_hash)
        if title is not None:
            location = "/tmp/bokeh_plot_{}_{}".format(title, random_hash)
    fig = create_rgb_split_figure(paths, title)
    output_file(location, title=title)
    show(fig)


def create_bw_all_5_plot(paths, title=None, location=None):
    """
    Given a list of paths, this will generate a html plot with an RGB image
    of the paths, and the channels plotted in separate facets

    Parameters:
    -----------
    - paths : list of strings
        image paths
    - title: string (default=None)
    - location: string (default=None)
        Where to save the html output, if None then this will be saved in /tmp

    Returns:
    --------
    Nothing, opens a html page in the web-browser saved at $location
    """
    if location is None:
        # save in /tmp/ with a random name
        random_hash = hex(random.getrandbits(32))
        location = "/tmp/bokeh_plot_{}.html".format(random_hash)
    fig = create_bw_all_5_figure(paths, title)
    output_file(location, title=title)
    show(fig)

def create_plot(paths, title=None, location=None, **kwargs):
    """
    Given a list of paths, this will generate a html plot with an RGB image
    of the paths and all 5 channels in greyscale

    Parameters:
    -----------
    - paths : list of strings
        image paths
    - title: string (default=None)
    - location: string (default=None)
        Where to save the html output, if None then this will be saved in /tmp

    Returns:
    --------
    Nothing, opens a html page in the web-browser saved at $location
    """
    if location is None:
        # save in /tmp/ with a random name
        random_hash = hex(random.getrandbits(32))
        location = "/tmp/bokeh_plot_{}.html".format(random_hash)
    fig = create_figure(paths, **kwargs)
    output_file(location, title=title)
    show(fig)


def plot_rgb(dataframe, index, path_col_prefix, channels, **kwargs):
    """
    plot images from a dataframe index

    Parameters:
    ------------
    - dataframe: pd.DataFrame
    - index: int
        row index for the observation to display images
    - path_col_prefix : string
    - channels : list of ints
    - **kwargs : additional arguments to create_rgb_split_plot()

    Returns:
    ---------
    Nothing, opens window a window in a web-browser

    Example:
    --------
        >>> interact.plot(my_data, index=100, path_col_prefix="URL_W",
                          channels=[3, 2, 1])
    """
    paths = path.get_paths(dataframe, index, path_col_prefix, channels)
    create_rgb_split_plot(paths, **kwargs)
    reset_output()


def plot_all_5(dataframe, index, path_col_prefix, **kwargs):
    """
    plot images from a dataframe index, uses all 5 channels plotted as
    greyscale images

    Parameters:
    ------------
    - dataframe: pd.DataFrame
    - index: int
        row index for the observation to display images
    - path_col_prefix : string
    - **kwargs : additional arguments to create_rgb_split_plot()

    Returns:
    ---------
    Nothing, opens window a window in a web-browser

    Example:
    --------
        >>> interact.plot(my_data, index=100, path_col_prefix="URL_W")
    """
    channels = range(1, 6)
    paths = path.get_paths(dataframe, index, path_col_prefix, channels)
    create_bw_all_5_plot(paths, **kwargs)
    reset_output()


def plot(dataframe, index, path_col_prefix, **kwargs):
    """
    plot images from a dataframe index, uses all 5 channels plotted as
    greyscale images, with an RGB image of channels [3, 5, 1] (because reasons)

    Parameters:
    ------------
    - dataframe: pd.DataFrame
    - index: int
        row index for the observation to display images
    - path_col_prefix : string
    - **kwargs : additional arguments to create_plot()

    Returns:
    ---------
    Nothing, opens window a window in a web-browser

    Example:
    --------
        >>> interact.plot(my_data, index=100, path_col_prefix="URL_W")
    """
    channels = range(1, 6)
    paths = path.get_paths(dataframe, index, path_col_prefix, channels)
    create_plot(paths, **kwargs)
    reset_output()
