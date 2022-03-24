#! python3
import enum
import logging
from typing import Optional, Set

log = logging.getLogger()

LEVEL_MAP = {
  'err': logging.ERROR,
  'warn': logging.WARNING,
  'info': logging.INFO,
  'dbg': logging.DEBUG,
}

def parse_args():
  from argparse import ArgumentParser

  parser = ArgumentParser()
  parser.add_argument('file', help='file to parse the original network matrix from')
  parser.add_argument('-l', '--log', help='set log level', choices=LEVEL_MAP.keys(), default='dbg')

  return parser.parse_args()

def format_id(id: int) -> str:
  CHARSET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
  LEN_CHARSET = len(CHARSET)

  if id < 0 or id > LEN_CHARSET:
    raise ValueError(f'id {id} outside of valid id bounds (min: 0, max: {LEN_CHARSET})')
  return CHARSET[id]

def get_link_id(a: str, b: str) -> tuple[str, str]:
  sort_ids = sorted([a, b])
  # return ''.join(sort_ids)
  return (sort_ids[0], sort_ids[1])

class Node:
  def __init__(self, vertice: str) -> None:
    self.vertice = vertice
    self.parent: Optional[Node] = None

  def __str__(self) -> str:
      if self.parent is not None:
        return f'{self.vertice}->{self.parent.vertice}'
      else:
        return f'{self.vertice}->null'

  def __repr__(self) -> str:
      return self.__str__()

  def tree(self) -> str:
    if self.parent is None:
      return self.vertice
    else:
      return f'{self.parent.tree()}->{self.vertice}'

def make_set(vertice: str) -> Node:
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
    x_root.parent = y_root

def kruskal(edges: list, vertices: Set[str]):
  l = log.getChild(kruskal.__name__)
  nodes = {vertice:make_set(vertice) for vertice in vertices}
  edges = [((nodes[edge[0][0]], nodes[edge[0][1]]),edge[1]) for edge in edges]
  edges = sorted(edges, key=lambda edge: edge[1])

  cost = 0
  tree = []

  l.debug(f'nodes={nodes}')
  l.debug(f'edges={edges}')
  for edge in edges:
    l.debug(f'current edges: {edge}')
    x, y = edge[0]
    l.debug(f'x={x}, y={y}')
    if find(x) != find(y):
      cost += edge[1]
      tree.append(edge)
      union(x, y)

  l.debug(tree)
  l.debug(nodes['A'].tree())
  return cost

if __name__ == '__main__':
  args = parse_args()
  logging.basicConfig(level=LEVEL_MAP[args.log])
  log.setLevel(LEVEL_MAP[args.log])
  log.info(f'set log level to {args.log}')

  edges = {}
  vertices = set()

  with open(args.file) as f:
    import csv

    matrix = csv.reader(f)
    matrix = [list(row) for row in matrix]

    log.debug('matrix: {}'.format(matrix))

    total_weight = 0

    for (row_id, row) in enumerate(matrix):
      row_id = format_id(row_id)

      vertices.add(row_id)

      for (col_id, weight) in enumerate(row):
        if weight == '-':
          continue
        col_id = format_id(col_id)
        weight = int(weight)

        link_id = get_link_id(row_id, col_id)

        vertices.add(col_id)

        log.debug(f'{row_id} -> {col_id} = {weight}')
        if link_id not in edges:
          edges[link_id] = weight
          total_weight += weight
        else:
          assert edges[link_id] == weight


    log.info(f'total weigth of the network is {total_weight}')
  log.debug(f'edges: {edges}')
  log.debug(f'vertices: {vertices}')
  reduced_weight = kruskal(edges.items(), vertices)
  log.info(f'reduce network weight: {reduced_weight}')
