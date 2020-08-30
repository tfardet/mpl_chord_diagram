"""
Tools to draw a chord diagram in python

License: MIT

Contributors:
* original author is fengwangPhysics (https://github.com/fengwangPhysics)
* improved arcs by cy1110 (https://github.com/cy1110)
* colormap support by pakitochus (https://github.com/pakitochus)
* refactoring by Silmathoron
"""

from collections.abc import Sequence

import matplotlib.patches as patches
from matplotlib.path import Path
from matplotlib.colors import ColorConverter

import numpy as np

LW = 0.3


def polar2xy(r, theta):
    return np.array([r*np.cos(theta), r*np.sin(theta)])


def initial_path(start, end, radius, width):
    ''' First 16 vertices and 15 instructions are the same for everyone '''
    if start > end:
        start, end = end, start

    start *= np.pi/180.
    end   *= np.pi/180.

    # optimal distance to the control points
    # https://stackoverflow.com/questions/1734745/
    # how-to-create-circle-with-b%C3%A9zier-curves
    # use 16-vertex curves (4 quadratic Beziers which accounts for worst case
    # scenario of 360 degrees)
    inner = radius*(1-width)
    opt   = 4./3. * np.tan((end-start)/ 16.) * radius
    inter1 = start*(3./4.)+end*(1./4.)
    inter2 = start*(2./4.)+end*(2./4.)
    inter3 = start*(1./4.)+end*(3./4.)

    verts = [
        polar2xy(radius, start),
        polar2xy(radius, start) + polar2xy(opt, start+0.5*np.pi),
        polar2xy(radius, inter1) + polar2xy(opt, inter1-0.5*np.pi),
        polar2xy(radius, inter1),
        polar2xy(radius, inter1),
        polar2xy(radius, inter1) + polar2xy(opt, inter1+0.5*np.pi),
        polar2xy(radius, inter2) + polar2xy(opt, inter2-0.5*np.pi),
        polar2xy(radius, inter2),
        polar2xy(radius, inter2),
        polar2xy(radius, inter2) + polar2xy(opt, inter2+0.5*np.pi),
        polar2xy(radius, inter3) + polar2xy(opt, inter3-0.5*np.pi),
        polar2xy(radius, inter3),
        polar2xy(radius, inter3),
        polar2xy(radius, inter3) + polar2xy(opt, inter3+0.5*np.pi),
        polar2xy(radius, end) + polar2xy(opt, end-0.5*np.pi),
        polar2xy(radius, end)
    ]

    codes = [
        Path.MOVETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.LINETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.LINETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.LINETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
    ]

    return start, end, verts, codes


def IdeogramArc(start, end, radius=1., width=0.2, color="r", alpha=0.7, ax=None):
    '''
    Draw an arc between two regions of the chord diagram.

    Parameters
    ----------
    start : float (degree in 0, 360)
        Starting degree.
    end : float (degree in 0, 360)
        Final degree.
    radius : float, optional (default: 1)
    width : float, optional (default: 0.2)
    ax : matplotlib axis, optional (default: not plot)
    color : valid matplotlib color, optional (default: "r")

    Returns
    -------
    verts, codes : lists
        Vertices and path instructions to draw the shape.
    '''
    start, end, verts, codes = initial_path(start, end, radius, width)

    opt    = 4./3. * np.tan((end-start)/ 16.) * radius
    inner  = radius*(1-width)
    inter1 = start*(3./4.)+end*(1./4.)
    inter2 = start*(2./4.)+end*(2./4.)
    inter3 = start*(1./4.)+end*(3./4.)

    verts += [
        polar2xy(inner, end),
        polar2xy(inner, end) + polar2xy(opt*(1-width), end-0.5*np.pi),
        polar2xy(inner, inter3) + polar2xy(opt*(1-width), inter3+0.5*np.pi),
        polar2xy(inner, inter3),
        polar2xy(inner, inter3),
        polar2xy(inner, inter3) + polar2xy(opt*(1-width), inter3-0.5*np.pi),
        polar2xy(inner, inter2) + polar2xy(opt*(1-width), inter2+0.5*np.pi),
        polar2xy(inner, inter2),
        polar2xy(inner, inter2),
        polar2xy(inner, inter2) + polar2xy(opt*(1-width), inter2-0.5*np.pi),
        polar2xy(inner, inter1) + polar2xy(opt*(1-width), inter1+0.5*np.pi),
        polar2xy(inner, inter1),
        polar2xy(inner, inter1),
        polar2xy(inner, inter1) + polar2xy(opt*(1-width), inter1-0.5*np.pi),
        polar2xy(inner, start) + polar2xy(opt*(1-width), start+0.5*np.pi),
        polar2xy(inner, start),
        polar2xy(radius, start),
    ]

    codes += [
        Path.LINETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.LINETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.LINETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.LINETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CLOSEPOLY,
    ]

    if ax is not None:
        path  = Path(verts, codes)
        patch = patches.PathPatch(path, facecolor=tuple(color) + (alpha,),
                                  edgecolor=tuple(color) + (alpha,), lw=LW)
        ax.add_patch(patch)

    return verts, codes


def ChordArc(start1, end1, start2, end2, radius=1.0, chordwidth=0.7, color=(1,0,0), alpha=0.7, ax=None):
    start1, end1, verts, codes = initial_path(start1, end1, radius, chordwidth)

    start2, end2, verts2, _ = initial_path(start2, end2, radius, chordwidth)

    rchord = radius * (1-chordwidth)

    verts += [polar2xy(rchord, end1), polar2xy(rchord, start2)] + verts2

    verts += [
        polar2xy(rchord, end2),
        polar2xy(rchord, start1),
        polar2xy(radius, start1),
    ]

    codes += [
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.LINETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.LINETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.LINETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
    ]

    if ax is not None:
        path = Path(verts, codes)
        patch = patches.PathPatch(path, facecolor=tuple(color)+(alpha,),
                                  edgecolor=tuple(color)+(alpha,), lw=LW)
        ax.add_patch(patch)

    return verts, codes


def selfChordArc(start=0, end=60, radius=1.0, chordwidth=0.7, color=(1,0,0), alpha=0.7, ax=None):
    start, end, verts, codes = initial_path(start, end, radius, chordwidth)
    
    rchord = radius * (1-chordwidth)

    verts += [
        polar2xy(rchord, end),
        polar2xy(rchord, start),
        polar2xy(radius, start),
    ]

    codes += [
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
    ]

    if ax is not None:
        path = Path(verts, codes)
        patch = patches.PathPatch(path, facecolor=tuple(color)+(alpha,),
                                  edgecolor=tuple(color)+(alpha,), lw=LW)
        ax.add_patch(patch)

    return verts, codes


def chordDiagram(X, ax, width=0.1, pad=2, chordwidth=0.7, colors=None,
                 cmap=None, alpha=0.7):
    """Plot a chord diagram

    Parameters
    ----------
    X :
        flux data, X[i, j] is the flux from i to j
    ax :
        matplotlib `axes` to show the plot
    colors : list, optional (default: from `cmap`)
        List of user defined colors or floats.
    cmap : str or colormap object (default: viridis)
        Colormap to use.
    width : optional
        width/thickness of the ideogram arc
    pad : optional
        gap pad between two neighboring ideogram arcs, unit: degree, default: 2 degree
    chordwidth : optional
        position of the control points for the chords, controlling the shape of the chords
    """
    import matplotlib.pyplot as plt

    # X[i, j]:  i -> j
    num_nodes = len(X)

    x = X.sum(axis = 1) # sum over rows
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    
    # First, set default to viridis color list
    if colors is None:
        colors = np.linspace(0, 1, num_nodes)

    if cmap is None:
        cmap = "viridis"

    if isinstance(colors, (Sequence, np.ndarray)):
        assert len(colors) == num_nodes, "One color per node is required."

        # check color type
        first_color = colors[0]

        if isinstance(first_color, (int, float, np.integer)):
            cm = plt.get_cmap(cmap)
            colors = cm(colors)[:, :3]
        else:
            colors = [ColorConverter.to_rgb(c) for c in colors]
    else:
        raise ValueError("`colors` should be a list.")

    # find position for each start and end
    y = x / np.sum(x).astype(float) * (360 - pad*len(x))

    pos = {}
    arc = []
    nodePos = []
    start = 0

    for i in range(len(x)):
        end = start + y[i]
        arc.append((start, end))
        angle = 0.5*(start+end)

        if -30 <= angle <= 210:
            angle -= 90
        else:
            angle -= 270

        nodePos.append(
            tuple(polar2xy(1.1, 0.5*(start + end)*np.pi/180.)) + (angle,))

        z = (X[i, :] / x[i].astype(float)) * (end - start)

        ids = np.argsort(z)

        z0 = start

        for j in ids:
            pos[(i, j)] = (z0, z0+z[j])
            z0 += z[j]

        start = end + pad

    for i in range(len(x)):
        start, end = arc[i]

        IdeogramArc(start=start, end=end, radius=1.0, color=colors[i],
                    width=width, alpha=alpha, ax=ax)

        start, end = pos[(i,i)]

        selfChordArc(start, end, radius=1 - width, chordwidth=chordwidth*0.7,
                     color=colors[i], alpha=alpha, ax=ax)

        for j in range(i):
            color = colors[i]

            if X[i, j] > X[j, i]:
                color = colors[j]

            start1, end1 = pos[(i,j)]
            start2, end2 = pos[(j,i)]

            ChordArc(start1, end1, start2, end2, radius=1 - width,
                     chordwidth=chordwidth, color=colors[i], alpha=alpha,
                     ax=ax)

    return nodePos


##################################
if __name__ == "__main__":
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(6,6))
    flux = np.array([[11975,  5871, 8916, 2868],
      [ 1951, 10048, 2060, 6171],
      [ 8010, 16145, 81090, 8045],
      [ 1013,   990,  940, 6907]
    ])

    ax = plt.axes([0,0,1,1])

    #nodePos = chordDiagram(flux, ax, colors=[hex2rgb(x) for x in ['#666666', '#66ff66', '#ff6666', '#6666ff']])
    nodePos = chordDiagram(flux, ax)
    ax.axis('off')
    prop = dict(fontsize=16*0.8, ha='center', va='center')
    nodes = ['non-crystal', 'FCC', 'HCP', 'BCC']
    for i in range(4):
        ax.text(nodePos[i][0], nodePos[i][1], nodes[i], rotation=nodePos[i][2], **prop)

    plt.show()

