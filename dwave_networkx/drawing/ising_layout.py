"""
Tools to visualize Ising problems and weighted graph problems on them.
"""

from __future__ import division

import networkx as nx
from networkx import draw

from dwave_networkx import _PY2
from dwave_networkx.drawing.draw_utilities import color_map


# compatibility for python 2/3
if _PY2:
    range = xrange
    itervalues = lambda d: d.itervalues()
    iteritems = lambda d: d.iteritems()
else:
    itervalues = lambda d: d.values()
    iteritems = lambda d: d.items()

__all__ = ['ising_layout', 'draw_ising']


def ising_layout(H, scale=1., center=None, dim=2):
    """Positions the nodes with given or generated layout

    NumPy (http://scipy.org) is required for this function.

    Parameters
    ----------
    H : graph
        A networkx graph. If every node in H has 'x' and 'y'
        attributes, then those are used to place the nodes. Otherwise will
        attempt to find positions, but is not guarunteed to succeed.

    scale : float (default 1.)
        Scale factor. When scale = 1 the all positions will fit within [0, 1]
        on the x-axis and [-1, 0] on the y-axis.

    center : None or array (default None)
        Coordinates of the top left corner.

    dim : int (default 2)
        Number of dimensions. When dim > 2, all extra dimensions are
        set to 0.

    Returns
    -------
    pos : dict
        A dictionary of x,y tuples keyed by node.

    Examples
    --------
    >>> J = {(0, 1): -1, (1, 2): -1, (2, 0): -1}
    >>> h = {0:-0.5,1:-1,2:0.0}
    >>> attr_dict = {0: {'x':0.0,'y':0.0}, 1: {'x':1.0,'y':0.0}, 2: {'x':0.0,'y':1.0}}
    >>> H =  dnx.ising_graph(h,J,attr_dict=attr_dict)
    >>> pos = dnx.ising_layout(H)

    """
    if not isinstance(H, nx.Graph):
        empty_graph = nx.Graph()
        empty_graph.add_nodes_from(H)
        H = empty_graph

    # best case scenario, each node in H has x and y attributes. Otherwise
    # we will try to determine it using a graph drawing heuristic.
    if all(set(['x','y']).issubset(dat) for __, dat in H.nodes(data=True)):
        node_xy = {v: (dat['x'],dat['y']) for v, dat in H.nodes(data=True)}
    else:
        node_xy = nx.random_layou(H)

    pos = node_xy

    return pos

def draw_ising(H, linear_biases={}, quadratic_biases={},
                 nodelist=None, edgelist=None, cmap=None, edge_cmap=None, vmin=None, vmax=None,
                 edge_vmin=None, edge_vmax=None,
                 **kwargs):
    """Draw Ising model graph H.

    If linear_biases and/or quadratic_biases are provided then the biases
    are visualized on the plot.

    Parameters
    ----------
    H : graph
        A networkx graph.

    linear_biases : dict (optional, default {})
        A dict of biases associated with each node in H. Should be of the
        form {node: bias, ...}. Each bias should be numeric.

    quadratic biases : dict (optional, default {})
        A dict of biases associated with each edge in H. Should be of the
        form {edge: bias, ...}. Each bias should be numeric. Self-loop
        edges are treated as linear biases.

    kwargs : optional keywords
       See networkx.draw_networkx() for a description of optional keywords.
       If linear_biases or quadratic_biases are provided, then
       any provided node_color or edge_color arguments are ignored.

    """

    if linear_biases or quadratic_biases:
        # if linear biases and/or quadratic biases are provided, then color accordingly.

        try:
            import matplotlib.pyplot as plt
            import matplotlib as mpl
        except ImportError:
            raise ImportError("Matplotlib and numpy required for draw_chimera()")

        if nodelist is None:
            nodelist = H.nodes()

        if edgelist is None:
            edgelist = H.edges()

        if cmap is None:
            cmap = plt.get_cmap('coolwarm')

        if edge_cmap is None:
            edge_cmap = plt.get_cmap('coolwarm')

        node_color, edge_color =  color_map(nodelist,edgelist,linear_biases,quadratic_biases)

        kwargs['edge_color'] = edge_color
        kwargs['node_color'] = node_color

        # the range of the color map is shared for nodes/edges and is symmetric
        # around 0.
        vmag = max(max(abs(c) for c in node_color), max(abs(c) for c in edge_color))
        if vmin is None:
            vmin = -1 * vmag
        if vmax is None:
            vmax = vmag
        if edge_vmin is None:
            edge_vmin = -1 * vmag
        if edge_vmax is None:
            edge_vmax = vmag

    draw(H, pos=ising_layout(H), nodelist=nodelist, edgelist=edgelist,
         cmap=cmap, edge_cmap=edge_cmap, vmin=vmin, vmax=vmax, edge_vmin=edge_vmin,
         edge_vmax=edge_vmax,
         **kwargs)

    # if the biases are provided, then add a legend explaining the color map
    if linear_biases or quadratic_biases:
        fig = plt.figure(1)
        # cax = fig.add_axes([])
        cax = fig.add_axes([.9, 0.2, 0.04, 0.6])  # left, bottom, width, height
        mpl.colorbar.ColorbarBase(cax, cmap=cmap,
                                  norm=mpl.colors.Normalize(vmin=-1 * vmag, vmax=vmag, clip=False),
                                  orientation='vertical')
