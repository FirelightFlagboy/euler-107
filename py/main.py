#! python3
import logging
from util import Edge, Network
import kruskal
import prim

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
    parser.add_argument('files', nargs='+', help='file to parse the original network matrix from')
    parser.add_argument('-l', '--log', help='set log level',
                        choices=LEVEL_MAP.keys(), default='info')

    return parser.parse_args()


def solve_file(filename: str):
    import copy
    initial_network = Network()

    with open(filename) as f:
        import csv

        matrix = csv.reader(f)
        matrix = [list(row) for row in matrix]

        for (rid, row) in enumerate(matrix):
            for (cid, weight) in enumerate(row):
                if weight == '-':
                    continue
                weight = int(weight)
                edge = Edge(rid, cid, weight)

                initial_network.insert_edge(edge)

    print('initial network:')
    initial_network.describe()

    print('kruskal network:')
    kruskal_network = kruskal.solve(copy.copy(initial_network))
    kruskal_network.describe()

    print('prim network:')
    prim_network = prim.solve(copy.copy(initial_network))
    prim_network.describe()


if __name__ == '__main__':
    args = parse_args()
    logging.basicConfig(level=LEVEL_MAP[args.log])
    log.setLevel(LEVEL_MAP[args.log])
    log.info(f'set log level to {args.log}')

    for filename in args.files:
        log.info(f'working on {filename}')
        solve_file(filename)
