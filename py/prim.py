import logging
from typing import Optional

from util import Edge, Network, Vertice

logger = logging.getLogger('prim')


def find_cheaper_edge(visited_vertices: list[Vertice], edges: list[Edge]) -> Optional[Edge]:
    log = logger.getChild(find_cheaper_edge.__name__)
    result = None
    for edge in edges:
        if edge.u in visited_vertices and edge.v not in visited_vertices:
            log.debug(f'potential link: {edge}, current: {result}')
            if result is None or result.cost > edge.cost:
                result = edge

    return result


def solve(network: Network) -> Network:
    log = logger.getChild(solve.__name__)

    edges = network.edges_sorted()
    vertices = network.vertices_sorted()
    vertices_count = len(vertices)

    log.debug(f'vertices_count={vertices_count}, vertices={vertices}')
    log.debug(f'edges_count={len(edges)}, edges={edges}')

    tree = Network()

    visited_vertices = [vertices[0]]  # include one vertice to start from

    for step in range(vertices_count - 1):
        log.debug(f'step {step}, visited_vertices {visited_vertices}')
        edge = find_cheaper_edge(visited_vertices, edges)
        if edge is not None:
            visited_vertices.append(edge.v)
            tree.insert_edge(edge)

    return tree
