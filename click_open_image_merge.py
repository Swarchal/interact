from open_equalize import open_equalize
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

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

    ix, iy = event.xdata, event.ydata
    print("INFO: clicked at ({0:5.2f}, {1:5.2f})".format(ix, iy))

    # calculate based on the axis extent, a reasonable distance
    # from the actual point in which the click has to occur
    ax = plt.gca()
    dx = fudge_factor * (ax.get_xlim()[1] - ax.get_xlim()[0])
    dy = fudge_factor * (ax.get_ylim()[1] - ax.get_ylim()[0])

    x = df[x_col]
    y = df[y_col]
    red_images = data[red].values.tolist()
    green_images = data[green].values.tolist()
    blue_images = data[blue].values.tolist()
    # check every point if the click was close enough to trigger
    for i in range(len(x)):
        if (x[i] > ix-dx and x[i] < ix+dx and y[i] > iy-dy and y[i] < iy+dy):
            print("INFO: close to point ({0:5.2f}, {1:5.2f})".format(x[i], y[i]))
            # create three separate rgb arrays
            r_arr = open_equalize(red_images[i])
            g_arr = open_equalize(green_images[i])
            b_arr = open_equalize(blue_images[i])
            plt.figure()
            rgb = np.dstack([r_arr, g_arr, b_arr])
            plt.imshow(rgb)
            if title is not None:
                img_title = df[title][i]
                plt.title(img_title)
            plt.axis("off")
            plt.show()
            break

fig.canvas.mpl_connect("button_press_event",
                       lambda event: onclick(event, data=df,
                                             x_col="x",
                                             y_col="y",
                                             red = "FullPath_W5",
                                             green = "FullPath_W4",
                                             blue = "FullPath_W1"))
plt.show()
