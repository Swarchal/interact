"""
utility functions
"""
import random
import numpy as np
from interact import path
from bokeh.plotting import figure, show, output_file
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
    # FIXME scaling is a bit weird, only seems to scale on the p_rgb figure
    # sizing_mode="scale_height"?
    plot = layout([[p_rgb, column_plots]], sizing_mode="scale_height")
    return plot



def create_rgb_split_plot(paths, title=None, location=None):
    """
    Given a list of paths, this will generate a html plot with an RGB image
    of the paths, and the channels plotted in separate facets

    Parameters:
    -----------
    paths : list of strings
        image paths
    title: string (default=None)
    location: string (default=None)
        Where to save the html output, if None then this will be saved in /tmp

    Returns:
    --------
    Nothing, opens a html page in the web-browser saved at $location
    """
    if location is None:
        # save in /tmp/ with a random name
        random_hash = hex(random.getrandbits(32))
        location = "/tmp/bokeh_plot_{}.html".format(random_hash)
    fig = create_rgb_split_figure(paths, title)
    output_file(location, title=title)
    show(fig)



def plot(dataframe, index, path_col_prefix, channels, **kwargs):
    """
    plot images from a dataframe index

    Parameters:
    ------------
    dataframe: pd.DataFrame
    index: int
        row index for the observation to display images
    path_col_prefix : string
    channels : list of ints
    **kwargs : additional arguments to create_rgb_split_plot()

    Returns:
    ---------
    Nothing, opens window a window in a web-browser
    """
    paths = path.get_paths(dataframe, index, path_col_prefix, channels)
    create_rgb_split_plot(paths, **kwargs)

