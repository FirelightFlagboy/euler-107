import logging
from typing import Optional

from util import Edge, Network, Vertice

logger = logging.getLogger('kruskal')


class Node:
    def __init__(self, vertice: Vertice) -> None:
        self.vertice = vertice
        self.parent: Optional[Node] = None
        self.rank = 0

    def __str__(self) -> str:
        if self.parent is not None:
            return f'{self.vertice}<-{self.parent.vertice}'
        else:
            return f'{self.vertice}<-null'

    def __repr__(self) -> str:
        return self.__str__()


class KruskalEdge:
    def __init__(self, u: Node, v: Node, edge: Edge) -> None:
        self.raw_edge = edge
        self.u = u
        self.v = v
        self.cost = edge.cost


def make_set(vertice: Vertice) -> Node:
    return Node(vertice)


def find(x: Node) -> Node:
    if x.parent is None:
        return x
    else:
        return x.parent


def union(x: Node, y: Node):
    x_root = find(x)
    y_root = find(y)

    if x_root != y_root:
        if x_root.rank < y_root.rank:
            x_root.parent = y_root
        else:
            y_root.parent = x_root
            if x_root.rank == y_root.rank:
                x_root.rank += 1


def solve(network: Network) -> Network:
    log = logger.getChild(solve.__name__)
    nodes = {vertice: make_set(vertice) for vertice in network.vertices_sorted()}
    edges = [KruskalEdge(nodes[edge.u], nodes[edge.v], edge) for edge in network.edges_sorted()]
    edges = sorted(edges, key=lambda edge: edge.cost)

    tree = Network()

    log.debug(f'len_nodes={len(nodes):2}, nodes={nodes}')
    log.debug(f'len_edges={len(edges):2}, edges={edges}')
    for edge in edges:
        log.debug(f'current edge: {edge.u.vertice}<->{edge.v.vertice}')
        if find(edge.u) != find(edge.v):
            tree.insert_edge(edge.raw_edge)
            union(edge.u, edge.v)
        else:
            log.debug(f'drop link {edge.u.vertice}<->{edge.v.vertice}')

    return tree
