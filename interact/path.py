"""
functions for fixing image file paths
"""

import os

def get_paths(dataframe, index, path_col_prefix, channel_numbers):
    """
    docstring
    Parameters:
    ------------
    dataframe: pd.dataframe
        DataFrame containing image path columns
    index : int
        row index
    path_col_prefix: str
        prefix for the columns containing image paths. e.g "URL_W"
    channel_numbers: list of ints
        numbers for append to the path_col_prefix, e.g [5, 4, 1] with the
        path_col_prefix = "URL_W", will become:
        ["URL_W5", "URL_W4", "URL_W1"]

    Returns:
    ---------
    list of strings (paths to 3 images)
    """
    # create path columns in correct order
    path_columns = [path_col_prefix + str(num) for num in channel_numbers]
    df_match = dataframe.loc[index, path_columns].values.tolist()
    return df_match


def get_end_path(path, last_n):
    """get the n elements of a path"""
    return os.sep.join(path.split(os.sep)[-last_n:])


def fix_path(path, prefix, last_n=4):
    """
    Given a broken path, and a prefix, append the last_n elements of the
    broken path to the prefix

    Parameters:
    -----------
    path : string
    prefix : string
    last_n : int

    Returns:
    ---------
    string in the form of the fixed path
    """
    suffix = get_end_path(path, last_n)
    return os.path.join(prefix, suffix)


def replace_paths(dataframe, cols, prefix, last_n):
    """
    replace paths in a dataframe with the correct prefix. This takes the last
    n elements from the original filename and prefixes them with the path
    in 'prefix'
    e.g original_path = "/wrong/path/exp/date/plate/date/img.tiff"
    the last 4 elements will be "date/plate/date/img.tiff"

    Parameters:
    -----------
    dataframe: pd.DataFrame
    cols : list of strings
        column names which contain the paths
    prefix : string
        what to prefix the file paths with
    last_n : int
        how many elements to keep from the suffix of the original path

    Returns:
    ---------
    dataframe with altered path columns


    Example:
    ---------
        >>> replace_paths(df, cols=["URL_W1", "URL_W2", "URL_W3"],
        >>>               prefix="/mnt/experiment_1", last_n=4)

    """
    return dataframe[cols].applymap(lambda x: fix_path(x, prefix, last_n))

