import numpy as np
from skimage import io
from skimage import exposure
from skimage import img_as_ubyte

def open_equalize(url, **kwargs):
    """open an image, equalize and transform to 8 bit"""
    return exposure.equalize_adapthist(img_as_ubyte(io.imread(url)), **kwargs)


def open_equalize_stack(list_of_urls, **kwargs):
    """open a list of channels and stack into a numpy array"""
    rgb = [open_equalize(url, **kwargs) for url in list_of_urls]
    return np.dstack(rgb)


def replace_paths(dataframe, cols, original, replacement):
    """
    Replace part of the paths in URLS in multiple columns of a dataframe.
    Useful for changing cluster image locations to local image locations.

    Parameters
    ------------
    cols : list-like
        list of column names containing URLS
    original : string
        string of part of path to be replaced
    replacement : string
        string to replace original in URLS

    Returns
    --------
    pandas.DataFrame of `cols` with replaced URLS
    """
    df_sub = dataframe[cols]
    return df_sub.applymap(lambda x: x.replace(original, replacement))


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

