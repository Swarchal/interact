from open_equalize import open_equalize
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def onclick(event, data, x_col, y_col, red, green, blue, title=None,
            fudge_factor = 0.025):
    """
    Click on point in matplotlib figure, create a merged RGB image associated
    with that point.

    Parameters:
    ------------
    event : click
    data : pandas DataFrame
    x_col : column relating to x-coord
    y_col : column relating to y-coord
    red : column name for red channel
    green : column name for green channel
    blue : column name for blue channel
    title : column name for image title
    fudge_factor : how close to a point to trigger as a click
    """

    # get click location
    ix, iy = event.xdata, event.ydata
    print("INFO: clicked at ({0:5.2f}, {1:5.2f})".format(ix, iy))
    # calculate based on the axis extent, a reasonable distance from the actual
    # point in which the click has to occur
    ax = plt.gca()
    dx = fudge_factor * (ax.get_xlim()[1] - ax.get_xlim()[0])
    dy = fudge_factor * (ax.get_ylim()[1] - ax.get_ylim()[0])
    x = data[x_col]
    y = data[y_col]
    colours = [red, green, blue]
    colours_data = [data[col] for col in colours]


    # check every point if the click was close enough to trigger
    for i in range(len(x)):
        if (x[i] > ix-dx and x[i] < ix+dx and y[i] > iy-dy and y[i] < iy+dy):
            print("INFO: close to point ({0:5.2f}, {1:5.2f})".format(x[i], y[i]))
            # create three separate colour arrays for RGB
            # equalize and convert intensity values to 8 bit integers otherwise
            # matplotlib goes all psychadelic
            # stack into a single array
            rgb_list = [open_equalize(col[i]) for col in colours_data]
            rgb = np.dstack(rgb_list)
            # plot
            plt.figure()
            plt.imshow(rgb)
            if title is not None:
                img_title = df[title][i]
                plt.title(img_title)
            plt.axis("off")
            plt.show()
            break

if __name__ == "__main__":

    plt.close("all")

    # create graph based on dataFrame with column for image URL
    df = pd.read_csv("df_paths2.csv")

    # generate x and y co-ordinates
    n_rows = df.shape[0]
    df["x"] = np.random.randn(n_rows)
    df["y"] = np.random.randn(n_rows)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(df.x, df.y, ".", alpha=0.25)
    ax.grid()


    fig.canvas.mpl_connect("button_press_event",
                           lambda event: onclick(event, data=df,
                                                 x_col="x",
                                                 y_col="y",
                                                 red = "FullPath_W5",
                                                 green = "FullPath_W4",
                                                 blue = "FullPath_W1"))
    plt.show()

