"""
Example file
"""

import os
import sys
sys.path = [os.path.abspath("..")] + sys.path

import matplotlib.pyplot as plt
import numpy as np

from mpl_chord_diagram import chord_diagram

# flux matrix

flux = np.array([
    [11975,  5871,  8916, 2868],
    [ 1951, 10048,  2060, 6171],
    [ 8010, 16145, 81090, 8045],
    [ 1013,   990,   940, 6907]
])

names = ['non-crystal', 'FCC', 'HCP', 'BCC']

example_arc_colors = [
    "#cc2233", "#2233cc", "orange", "gray",
    "#ffcc00", "#00ffcc", "purple", "green",
    "#00FF00", "#FF00FF", "#FFFF00", "#00FFFF",
    "#FF0000", "#0000FF", "#800000", "#000080",
]




# plot different examples

grads = (True, False, False, False, False)                  # gradient
gaps  = (0.03, 0, 0.03, 0, 0.1)                             # gap value
sorts = ("size", "distance", None, "distance", None)        # sort type
iclrs = (None, None, None, None, "slategray")               # ideogram colors
cclrs = (None, None, "slategrey", None, example_arc_colors) # chord colors
nrota = (False, False, True, True, False)                   # name rotation
cmaps = (None, None, None, "summer", None)                  # colormap
fclrs = "grey"                                              # fontcolors
drctd = (False, False, False, True, True)                   # directed

args = (grads, gaps, sorts, iclrs, cclrs, nrota, cmaps, drctd)

for grd, gap, srt, ic, cc, nr, cm, d in zip(*args):
    chord_diagram(flux, names, gap=gap, use_gradient=grd, sort=srt, directed=d,
                  cmap=cm, ideogram_colors=ic, chord_colors=cc, rotate_names=nr, fontcolor=fclrs)

    str_grd = "_gradient" if grd else ""

    plt.savefig(
        "images/example{}_sort-{}{}.png".format(str_grd, srt,
                                                "_directed" if d else ""),
        dpi=600, transparent=True, bbox_inches='tight',
        pad_inches=0.02)

plt.show()


# plot with partial circle

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

keep = list(range(len(flux) - 1))

total = flux.sum()
partial = flux[keep][:, keep].sum()

colors = ["#cc2233", "#2233cc", "orange", "gray"]

chord_diagram(flux, names, ax=ax1, colors=colors, start_at=60)
chord_diagram(flux[keep][:, keep], names[:-1], ax=ax2, colors=colors[:-1],
              start_at=60, extent=360*partial/total)

plt.show()


# min chord width zero reciprocals

flux = np.array([
    [11975,  5871,  8916,     0],
    [ 1951,     0,  2060,     0],
    [ 8010, 16145,  3504,     0],
    [    0,  5200,   300,  6907]
])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

chord_diagram(flux, names, ax=ax1)
chord_diagram(flux, names, ax=ax2, min_chord_width=200)

plt.show()
