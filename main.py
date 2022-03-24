#! python3
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


if __name__ == '__main__':
  args = parse_args()
  logging.basicConfig(level=LEVEL_MAP[args.log])
  log = logging.getLogger(__name__)
  log.info(f'set log level to {args.log}')

  with open(args.file) as f:
    import csv

    matrix = csv.reader(f)

    for row in matrix:
        print(', '.join(row))
