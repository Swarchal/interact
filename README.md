# interact

Interactive plots and visualisations for relating data points back to the images that generated them.

Very much a work in progress.


```python
from plot_interact import plot_interactive
import pandas as import pd

df = pd.read_csv("../data/df_paths2.csv")

# channel list (red, green, blue)
channels = ["FullPath_W5", "FullPath_W4", "FullPath_W1"]
plot_interactive(df, "x", "y", channels)
```

<img src="/graphics/screenshot.png" height="500">


## TODO:

- [x] Merge separate channels
- [x] Normalise intensity histograms
- [x] Create functions to make graphs on the fly from a pandas.DataFrame
- [x] Pass RGB columns as list
- [ ] Ability to plot 2 channels
- [ ] Categorically coloured plots
- [ ] Continuously coloured plots
