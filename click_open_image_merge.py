import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from skimage import exposure
from skimage import img_as_ubyte
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
ax.plot(df.x, df.y, ".", alpha=0.5)


def onclick(event, data, x_col, y_col, red, green, blue):
    """
    trigger event when click close to a point in a matplotlib figure

    Parameters:
    ------------
    event : click
    data : pandas DataFrame
    x_col : column relating to x-coord
    y_col : column relating to y-coord
    img_tab : column listing image URLs
    """

    ix, iy = event.xdata, event.ydata
    print("clicked at x={0:5.2f}, y={1:5.2f}".format(ix, iy))

    # calculate based on the axis extent, a reasonable distance
    # from the actual point in which the click has to occur (2.5%)
    ax = plt.gca()
    dx = 0.025 * (ax.get_xlim()[1] - ax.get_xlim()[0])
    dy = 0.025 * (ax.get_ylim()[1] - ax.get_ylim()[0])
    
    x = df[x_col]
    y = df[y_col]
    red_images = data[red].values.tolist()
    green_images = data[green].values.tolist()
    blue_images = data[blue].values.tolist()
    # check every point if the click was close enough to trigger
    for i in range(len(x)):
        if (x[i] > ix-dx and x[i] < ix+dx and y[i] > iy-dy and y[i] < iy+dy):
            #print("opening {}".format(images[i]))
            r_arr = exposure.equalize_adapthist(img_as_ubyte(io.imread(red_images[i])))
            g_arr = exposure.equalize_adapthist(img_as_ubyte(io.imread(green_images[i])))
            b_arr = exposure.equalize_adapthist(img_as_ubyte(io.imread(blue_images[i])))
            # create three separate rgb arrays
            plt.figure()
            rgb = np.dstack([r_arr, g_arr, b_arr])
            plt.imshow(rgb)
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
