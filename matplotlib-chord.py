"""
Tools to draw a chord diagram in python
"""

from collections.abc import Sequence

import matplotlib.patches as patches

from matplotlib.colors import ColorConverter, LinearSegmentedColormap
from matplotlib.path import Path

import numpy as np


LW = 0.3


def dist(points):
    x1, y1 = points[0]
    x2, y2 = points[1]

    return np.sqrt((x2 - x1)*(x2 - x1) + (y2 - y1)*(y2 - y1))


def linear_gradient(cstart, cend, n=10):
    '''
    Return a gradient list of `n` colors going from `cstart` to `cend`.
    '''
    s = np.array(ColorConverter.to_rgb(cstart))
    f = np.array(ColorConverter.to_rgb(cend))

    rgb_list = [s + (t / (n - 1))*(f - s) for t in range(n)]

    return rgb_list


def gradient(start, end, color1, color2, meshgrid, mask, ax, alpha):
    '''
    Create a linear gradient from `start` to `end`, which is translationally
    invarient in the orthogonal direction.
    The gradient is then cliped by the mask.
    '''
    xs, ys = start
    xe, ye = end

    Z = None

    X, Y = meshgrid

    # get the orthogonal projection of each point on the gradient start line
    if np.isclose(ye, ys):
        Z = np.clip((X - xs) / (xe - xs), 0, 1)
    else:
        Yh = ys

        if not np.isclose(xe, xs):
            norm = np.sqrt((ye-ys)*(ye-ys) / ((xe-xs)*(xe-xs)) + 1)

            Yh = ys + ((ys - ye)*(X - xs)/(xe - xs) + (Y - ys)) / norm

        # generate the image, varying from 0 to 1
        Z = np.clip((Y - Yh) / (ye - ys), 0, 1)

    # generate the colormap
    n_bin = 100

    color_list = linear_gradient(color1, color2, n_bin)

    cmap = LinearSegmentedColormap.from_list("gradient", color_list, N=n_bin)

    im = ax.imshow(Z, interpolation='bilinear', cmap=cmap,
                   origin='lower', extent=[-1, 1, -1, 1],
                   clip_path=mask, clip_on=True, alpha=alpha)

    # ~ im = ax.imshow(Z, interpolation='bilinear', cmap=cmap,
                   # ~ origin='lower', extent=[-1, 1, -1, 1], alpha=alpha)

    im.set_clip_path(mask)


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


def ChordArc(start1, end1, start2, end2, radius=1.0, chordwidth=0.7,
             color="r", cend="r", alpha=0.7, ax=None, use_gradient=False):
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

        if use_gradient:
            # find the start and end points of the gradient
            p0 = np.array([verts[0], verts[-4]])
            p1 = np.array([verts[15], verts[18]])

            points = p0 if dist(p0) < dist(p1) else p1

            # make the patch
            patch = patches.PathPatch(path, facecolor="none",
                                      edgecolor="none", lw=LW)
            ax.add_patch(patch)  # this is required to clip the gradient

            # make the grid
            x = y = np.linspace(-1, 1, 50)
            meshgrid = np.meshgrid(x, y)

            gradient(points[0], points[1], color, cend, meshgrid, patch, ax,
                     alpha)
        else:
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


def selfChordArc(start=0, end=60, radius=1.0, chordwidth=0.7, ax=None, color=(1,0,0), alpha=0.7):
    # start, end should be in [0, 360)
    if start > end:
        start, end = end, start
    start *= np.pi/180.
    end *= np.pi/180.
    opt = 4./3. * np.tan((end-start)/ 16.) * radius #16-vertex curves (4 quadratic Beziers which accounts for worst case scenario of 360 degrees)
    inter1 = start*(3./4.)+end*(1./4.)
    inter2 = start*(2./4.)+end*(2./4.)
    inter3 = start*(1./4.)+end*(3./4.)
    rchord = radius * (1-chordwidth)
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
        polar2xy(radius, end),
        polar2xy(rchord, end),
        polar2xy(rchord, start),
        polar2xy(radius, start),
        ]

    codes = [Path.MOVETO,
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


def chordDiagram(X, width=0.1, pad=2., chordwidth=0.7, colors=None,
                 cmap=None, alpha=0.7, ax=None, use_gradient=False):
    """
    Plot a chord diagram.
    Parameters
    ----------
    X : square matrix
        Flux data, X[i, j] is the flux from i to j
    width : float, optional (default: 0.1)
        Width/thickness of the ideogram arc.
    pad : float, optional (default: 2)
        Gap pad between two neighboring ideogram arcs. Unit: degree.
    chordwidth : float, optional (default: 0.7)
        Position of the control points for the chords, controlling their shape.
    colors : list, optional (default: from `cmap`)
        List of user defined colors or floats.
    cmap : str or colormap object (default: viridis)
        Colormap to use.
    alpha : float in [0, 1], optional (default: 0.7)
        Opacity of the chord diagram.
    ax : matplotlib axis, optional (default: new axis)
        Matplotlib axis where the plot should be drawn.
    use_gradient : bool, optional (default: False)
        Whether a gradient should be use so that chord extremities have the
        same color as the arc they belong to.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots()

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

        color = colors[i]

        for j in range(i):
            cend = colors[j]

            start1, end1 = pos[(i,j)]
            start2, end2 = pos[(j,i)]

            ChordArc(start1, end1, start2, end2, radius=1 - width,
                     chordwidth=chordwidth, color=colors[i], cend=cend,
                     alpha=alpha, ax=ax, use_gradient=use_gradient)

    # configure axis
    ax.set_aspect(1)
    ax.axis('off')
    plt.tight_layout()

    return nodePos


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    flux = np.array([[11975,  5871, 8916, 2868],
      [ 1951, 10048, 2060, 6171],
      [ 8010, 16145, 81090, 8045],
      [ 1013,   990,  940, 6907]
    ])

    for grd in (True, False):
        _, ax = plt.subplots(figsize=(6, 6))

        nodePos = chordDiagram(flux, ax=ax, use_gradient=grd)
        
        prop = dict(fontsize=16*0.8, ha='center', va='center')
        nodes = ['non-crystal', 'FCC', 'HCP', 'BCC']

        for i in range(len(flux)):
            ax.text(nodePos[i][0], nodePos[i][1], nodes[i],
                    rotation=nodePos[i][2], **prop)

        plt.savefig("example{}.png".format("_gradient" if grd else ""),
                    dpi=600, transparent=True, bbox_inches='tight',
                    pad_inches=0.02)

    plt.show()
