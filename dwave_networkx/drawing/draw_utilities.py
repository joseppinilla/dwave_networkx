"""
A collection of utility functions useful for DWave Networkx drawing.
"""

import sys

__all__ = ['color_map']

PY2 = sys.version_info[0] == 2
if PY2:
    iteritems = lambda d: d.iteritems()
    itervalues = lambda d: d.itervalues()
else:
    iteritems = lambda d: d.items()
    itervalues = lambda d: d.values()


def color_map(nodelist, edgelist, linear_biases, quadratic_biases):
    # any edges or nodes with an unspecified bias default to 0
    def edge_color(u, v):
        c = 0.
        if (u, v) in quadratic_biases:
            c += quadratic_biases[(u, v)]
        if (v, u) in quadratic_biases:
            c += quadratic_biases[(v, u)]
        return c

    def node_color(v):
        c = 0.
        if v in linear_biases:
            c += linear_biases[v]
        if (v, v) in quadratic_biases:
            c += quadratic_biases[(v, v)]
        return c

    node_color = [node_color(v) for v in nodelist]
    edge_color = [edge_color(u, v) for u, v in edgelist]

    return node_color, edge_color
