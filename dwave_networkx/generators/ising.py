"""
Generators for some graphs derived from the D-Wave System.

"""
import networkx as nx
from networkx.algorithms.bipartite import color
from networkx import diameter

from dwave_networkx import _PY2
from dwave_networkx.exceptions import DWaveNetworkXException

__all__ = ['ising_graph']

# compatibility for python 2/3
if _PY2:
    range = xrange

def ising_graph(h={}, J={}, attr_dict=None, create_using=None):
    """Creates an Ising graph from the adjacency matrix.

    An Ising model is an undirected d-dimensional graph of a lattice,
    with the nodes representing site spins with external magnetic fields
    h, and with edges representing site interactions J.

    Parameters
    ----------
    h (dict/list): The linear terms in the Ising problem. If a
        dict, should be of the form {v: bias, ...} where v is
        a variable in the Ising problem, and bias is the linear
        bias associated with v. If a list, should be of the form
        [bias, ...] where the indices of the biases are the
        variables in the Ising problem.
    J (dict): A dictionary of the quadratic terms in the Ising
        problem. Should be of the form {(u, v): bias} where u,
        v are variables in the Ising problem and bias is the
        quadratic bias associated with u, v.
    create_using : Graph, optional (default None)
        If provided, this graph is cleared of nodes and edges and filled
        with the new graph. Usually used to set the type of the graph.


    Returns
    -------
    H : a NetworkX Weighted Graph
        An Ising lattice. Nodes are labeled by integers.
        Edges and nodes are weighted using the 'bias' attribute.


    Examples
    ========
    >>> H = dnx.ising_graph()  # a single Chimera tile

    """
    H = nx.empty_graph(0, create_using)

    H.name = "ising_graph"

    H.add_edges_from(J)

    nx.set_edge_attributes(H,J,'bias')
    nx.set_node_attributes(H,h,'bias')

    if attr_dict:
        nx.set_node_attributes(H,attr_dict)

    return H
