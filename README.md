# mpl-chord-diagram

[![License: MIT](https://img.shields.io/badge/license-MIT-green)](./LICENSE)
[![PyPI](https://img.shields.io/pypi/v/mpl-chord-diagram)](https://pypi.org/project/mpl-chord-diagram)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6583470.svg)](https://doi.org/10.5281/zenodo.6583470)


Python module to plot chord diagrams with [matplotlib](https://matplotlib.org).

The code is hosted on [Codeberg's Gitea](https://codeberg.org/tfardet/mpl_chord_diagram)
and mirrored on [GitHub](https://github.com/tfardet/mpl_chord_diagram).
Please raise any issue you encouter on the [issue tracker](https://codeberg.org/tfardet/mpl_chord_diagram/issues).

Note that the repository has this structure (everything is on root level) to
be able to be used more easily as a git submodule.

## Example

An example can be found in file `example.py`.
Here is what the diagrams look like:
* Upper left  > no gradient, no gap, default colormap, chords sorted by distance
* Upper right > directed chords, no gap, "summer" colormap, rotated names, chords sorted by distance
* Lower left  > gap, single color for chords, rotated names, unsorted chords
* Lower right > gradient and gap, default colormap, chords sorted by size

<img src="https://codeberg.org/tfardet/mpl_chord_diagram/media/branch/main/images/example_sort-distance.png" width="390"
     alt="Chord diagram without gradient, chords sorted by distance"><img
     src="https://codeberg.org/tfardet/mpl_chord_diagram/media/branch/main/images/example_sort-distance_directed.png" width="390"
     alt="Chord diagram with directed chords and rotated names, chords sorted by distance">

<img src="https://codeberg.org/tfardet/mpl_chord_diagram/media/branch/main/images/example_sort-None.png" width="390"
     alt="Chord diagram without grey chords in unsorted order"><img
     src="https://codeberg.org/tfardet/mpl_chord_diagram/media/branch/main/images/example_gradient_sort-size.png" width="390"
     alt="Chord diagram with gradient, sorted by size">


## Main plot function

```python
def chord_diagram(mat, names=None, order=None, sort="size", directed=False,
                  colors=None, cmap=None, use_gradient=False, chord_colors=None,
                  alpha=0.7, start_at=0, extent=360, width=0.1, pad=2., gap=0.03,
                  chordwidth=0.7, min_chord_width=0, fontsize=12.8,
                  fontcolor="k", rotate_names=False, ax=None, show=False):
    """
    Plot a chord diagram.

    Draws a representation of many-to-many interactions between elements, given
    by an interaction matrix.
    The elements are represented by arcs proportional to their degree and the
    interactions (or fluxes) are drawn as chords joining two arcs:

    * for undirected chords, the size of the arc is proportional to its
      out-degree (or simply its degree if the matrix is fully symmetrical), i.e.
      the sum of the element's row.
    * for directed chords, the size is proportional to the total-degree, i.e.
      the sum of the element's row and column.

    Parameters
    ----------
    mat : square matrix
        Flux data, ``mat[i, j]`` is the flux from i to j.
    names : list of str, optional (default: no names)
        Names of the nodes that will be displayed (must be ordered as the
        matrix entries).
    order : list, optional (default: order of the matrix entries)
        Order in which the arcs should be placed around the trigonometric
        circle.
    sort : str, optional (default: "size")
        Order in which the chords should be sorted: either None (unsorted),
        "size" (default, drawing largest chords first), or "distance"
        (drawing the chords of the two closest arcs at each end of the current
        arc, then progressing towards the connexions with the farthest arcs in
        both drections as we move towards the center of the current arc).
    directed : bool, optional (default: False)
        Whether the chords should be directed, like edges in a graph, with one
        part of each arc dedicated to outgoing chords and the other to incoming
        ones.
    colors : list, optional (default: from `cmap`)
        List of user defined colors or floats.
    cmap : str or colormap object (default: viridis)
        Colormap that will be used to color the arcs and chords by default.
        See `chord_colors` to use different colors for chords.
    use_gradient : bool, optional (default: False)
        Whether a gradient should be use so that chord extremities have the
        same color as the arc they belong to.
    chord_colors : str, or list of colors, optional (default: None)
        Specify color(s) to fill the chords differently from the arcs.
        When the keyword is not used, chord colors default to the colomap given
        by `colors`.
        Possible values for `chord_colors` are:

        * a single color (do not use an RGB tuple, use hex format instead),
          e.g. "red" or "#ff0000"; all chords will have this color
        * a list of colors, e.g. ``["red", "green", "blue"]``, one per node
          (in this case, RGB tuples are accepted as entries to the list).
          Each chord will get its color from its associated source node, or
          from both nodes if `use_gradient` is True.
    alpha : float in [0, 1], optional (default: 0.7)
        Opacity of the chord diagram.
    start_at : float, optional (default : 0)
        Location, in degrees, where the diagram should start on the unit circle.
        Default is to start at 0 degrees, i.e. (x, y) = (1, 0) or 3 o'clock),
        and move counter-clockwise
    extent : float, optional (default : 360)
        The angular aperture, in degrees, of the diagram.
        Default is to use the whole circle, i.e. 360 degrees, but in some cases
        it can be useful to use only a part of it.
    width : float, optional (default: 0.1)
        Width/thickness of the ideogram arc.
    pad : float, optional (default: 2)
        Distance between two neighboring ideogram arcs. Unit: degree.
    gap : float, optional (default: 0)
        Distance between the arc and the beginning of the cord.
    chordwidth : float, optional (default: 0.7)
        Position of the control points for the chords, controlling their shape.
    min_chord_width : float, optional (default: 0)
        Minimal chord width to replace small entries and zero reciprocals in
        the matrix.
    fontsize : float, optional (default: 12.8)
        Size of the fonts for the names.
    fontcolor : str or list, optional (default: black)
        Color of the fonts for the names.
    rotate_names : (list of) bool(s), optional (default: False)
        Whether to rotate all names (if single boolean) or some of them (if
        list) by 90°.
    ax : matplotlib axis, optional (default: new axis)
        Matplotlib axis where the plot should be drawn.
    show : bool, optional (default: False)
        Whether the plot should be displayed immediately via an automatic call
        to `plt.show()`.
    """
```


## Usage and requirements

Install using

    pip install mpl-chord-diagram

then, in python script or terminal:

```python
from mpl_chord_diagram import chord_diagram
```

The code requires ``numpy``, ``scipy`` and ``matplotlib``, which should be
installed automatically. If necessary, you can also install them by calling

    pip install -r requirements.txt


## Citing mpl-chord-diagram

Please cite our Zenodo DOI
([10.5281/zenodo.6583470](https://doi.org/10.5281/zenodo.6583470)) if you use
this library.

**Libraries using mpl-chord-diagram:**

* [NNGT](https://nngt.readthedocs.io) (graph theory)
* [mdciao](https://proteinformatics.uni-leipzig.de/mdciao) (proteomics)


## Contributors

* Maintainers:
   - [Tanguy Fardet](https://tfardet.srht.site)
   - [Guillermo Pérez-Hernández](https://codeberg.org/gph82), [gph82](https://github.com/gph82)
* Original author: [@fengwangPhysics](https://github.com/fengwangPhysics)
* Other contributors:
   - [@pakitochus](https://github.com/pakitochus)
   - [@cy1110](https://github.com/cy1110)


## Alternative solutions in Python

The [chord diagram](https://moshi4.github.io/pyCirclize/chord_diagram/) option
of [pyCirclize](https://moshi4.github.io/pyCirclize/).

See also the Python Graph Gallery's
[chord diagram entry](https://www.python-graph-gallery.com/chord-diagram/) for
alternative libraries.
