import argparse
import logging
from rounders.csv_rounder import csv_rounder


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Smartly rounding percentages in batch from a CSV file.'
    )
    parser.add_argument(
        '-n',
        '--no-total-col',
        dest='has_total_col',
        action='store_false',
        default=True,
        help='Set this flag if there is no total column in the file.'
    )
    parser.add_argument(
        'file_path',
        nargs='+',
        help='The path(s) of the target CSV file(s)'
    )
    args = parser.parse_args()
    for path in args.file_path:
        logging.info(f'Rounding the percentages in CSV file {path}...')
        csv_rounder(path, args.has_total_col)
