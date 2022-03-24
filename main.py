#! python3
import enum
import logging

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

def get_link_id(a: str, b: str) -> str:
  return ''.join(sorted([a, b]))

if __name__ == '__main__':
  args = parse_args()
  logging.basicConfig(level=LEVEL_MAP[args.log])
  log = logging.getLogger(__name__)
  log.info(f'set log level to {args.log}')

  raw_network = {}

  with open(args.file) as f:
    import csv

    matrix = csv.reader(f)
    matrix = [list(row) for row in matrix]

    log.debug('matrix: {}'.format(matrix))

    total_weight = 0

    for (row_id, row) in enumerate(matrix):
      row_id = format_id(row_id)

      for (col_id, weight) in enumerate(row):
        if weight == '-':
          continue
        col_id = format_id(col_id)
        weight = int(weight)

        link_id = get_link_id(row_id, col_id)

        log.debug(f'{row_id} -> {col_id} = {weight}')
        if link_id not in raw_network:
          raw_network[link_id] = weight
          total_weight += weight
        else:
          assert raw_network[link_id] == weight


    log.info(f'total weigth of the network is {total_weight}')
  log.debug(f'raw_network: {raw_network}')
