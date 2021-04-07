"""
Example file
"""

import os
import sys
sys.path.append(os.path.abspath(".."))

import matplotlib.pyplot as plt
import numpy as np

from mpl_chord_diagram import chord_diagram

# flux matrix

flux = np.array([
    [11975,  5871, 8916, 2868],
    [ 1951, 10048, 2060, 6171],
    [ 8010, 16145, 81090, 8045],
    [ 1013,   990,  940, 6907]
])

names = ['non-crystal', 'FCC', 'HCP', 'BCC']

# plot different examples

grads = (True, False, False, True)                # gradient
gaps  = (0.03, 0, 0.03, 0)                        # gap value
sorts = ("size", "size", "distance", "distance")  # sort type
cclrs = (None, None, "slategrey", None)           # chord colors
nrota = (False, False, True, True)                # name rotation
cmaps = (None, None, None, "summer")              # colormap
fclrs = "grey"                                    # fontcolors

for grd, gap, srt, cc, nr, cm in zip(grads, gaps, sorts, cclrs, nrota, cmaps):
    chord_diagram(flux, names, gap=gap, use_gradient=grd, sort=srt,
                  cmap=cm, chord_colors=cc, rotate_names=nr, fontcolor=fclrs)

    str_grd = "_gradient" if grd else ""

    plt.savefig(
        "images/example{}_sort-{}.png".format(str_grd, srt),
                dpi=600, transparent=True, bbox_inches='tight',
                pad_inches=0.02)

plt.show()
