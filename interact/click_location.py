import numpy as np
import matplotlib.pyplot as plt


def onclick_locate(event):
    ix, iy = event.xdata, event.ydata
    print("clicked at x={0:5.2f}, y={1:5.2f}".format(ix, iy))

    # calculate based on the axis extent, a reasonable distance
    # from the actual point in which the click has to occur (2.5%)
    ax = plt.gca()
    dx = 0.025 * (ax.get_xlim()[1] - ax.get_xlim()[0])
    dy = 0.025 * (ax.get_ylim()[1] - ax.get_ylim()[0])

    # check for every point if the click was close enough to trigger
    for i in range(len(x)):
        if (x[i] > ix-dx and x[i] < ix+dx and y[i] > iy-dy and y[i] < iy+dy):
            print(i)
            print("clicked close to point {}, {}".format(x[i], y[i]))

if __name__ == "__main__":

    plt.close("all")
    x = np.random.randn(200)
    y = np.random.randn(200)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x, y, "o", alpha=0.7)
    cid = fig.canvas.mpl_connect("button_press_event", onclick_locate)
    plt.show()

