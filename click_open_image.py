import numpy as np
import matplotlib.pyplot as plt
from skimage import io
import pandas as pd

plt.close("all")

# create graph based on dataFrame with column for image URL

df = pd.read_csv("test_df.csv")
x = df["V1"]
y = df["V2"]

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(x, y, ".", alpha=0.5)

def onclick(event, data, x_col, y_col, img_tag):
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
    images = data[img_tag].values.tolist()
    # check every point if the click was close enough to trigger
    for i in range(len(x)):
        if (x[i] > ix-dx and x[i] < ix+dx and y[i] > iy-dy and y[i] < iy+dy):
            print("opening {}".format(images[i]))
            img_array = io.imread(images[i])
            plt.figure()
            plt.imshow(img_array, cmap=plt.cm.Greys_r)
            plt.show()
            break

fig.canvas.mpl_connect("button_press_event",
                             lambda event: onclick(event, data=df,
                                                   x_col="V1",
                                                   y_col="V2",
                                                   img_tag = "FullPath_W1"))
plt.show()
