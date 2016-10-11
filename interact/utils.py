import pandas as pd
from skimage import io
from skimage import exposure
from skimage import img_as_ubyte

def open_equalize(url, **kwargs):
    """ open an image, equalize and transform to 8 bit """
    return exposure.equalize_adapthist(img_as_ubyte(io.imread(url)), **kwargs)


def replace_paths(df, cols, original, replacement):
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
    df_sub = df[cols]
    return df_sub.applymap(lambda x: x.replace("original", "replacement"))
