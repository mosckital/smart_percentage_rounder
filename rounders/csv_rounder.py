"""
This script provides methods to apply the smart percentage rounding in batch
to the data in a CSV file.
"""
import csv
import argparse
import logging
from os.path import basename, dirname, join
from rounders.rounder import original_rounder
from typing import Sequence, Union, Optional


def csv_rounder(csv_path: str, has_total_col: bool = False):
    """
    To apply the percentage conversion and the smart percentage rounding to all
    lines in the provided csv file and save the results in a file.

    :param csv_path: the path to the input CSV file
    :param has_total_col: `True` if the last data column is a total column
    :return: the path to the result CSV file
    """
    # extract directory and input file name
    csv_dir, file_name = dirname(csv_path), basename(csv_path)
    # construct output file name and path
    output_parts = file_name.split('.')
    output_parts.insert(-1, 'out')
    output_name = '.'.join(output_parts)
    output_path = join(csv_dir, output_name)
    # apply the smart rounding one line by one line
    with open(csv_path, newline='') as input_file, open(output_path, 'w', newline='') as output_file:
        reader = csv.reader(input_file)
        writer = csv.writer(output_file)
        for line, row in enumerate(reader):
            writer.writerow(row_rounder(row, line, has_total_col=has_total_col))
        return output_path


def row_rounder(row: Sequence[str], line: Optional[int], has_total_col: bool = False) -> Sequence[Union[str, float]]:
    """
    To convert the data in a CSV row to percentages and then smartly round the
    percentages to no decimal with a guarantee that the sum of rounded
    percentages is 100%.

    The row can have up to three parts:
    [title column(s)] | data columns | [empty trailing column(s)]

    Only the data columns will be applied the smart rounding and the other two
    parts will keep unchanged in the return result.
    If `has_total_col` has been set to True, the last column of the data columns
    will be considered as the total column and not involve into the percentage
    conversion and smart rounding.

    :param row: the line to apply the smart rounding
    :param line: the line number
    :param has_total_col: `True` if the last data column is a total column
    :return: the smartly rounded line in CSV format
    """
    data, empty_tail, result = [], [], []
    last_data_field = None
    for field in row:
        try:
            # float conversion may fail in the two optional parts of the row
            val = float(field)
            data.append(val)
            last_data_field = field
        except ValueError:
            if data:
                # after data part, so in the trailing column(s) part
                if not field.strip():
                    empty_tail.append(field)
                else:
                    # cannot have any quoted field after the start of numeric fields
                    raise RuntimeError(f'CSV file malformed at line {line}!')
            else:
                # before data part, so in the title column(s) part
                result.append(field)
    # construct the return result
    if data:
        if has_total_col:
            result.extend(original_rounder(data[:-1]))
            # to use the original string instead of the converted float
            # as it may be originally an int
            result.append(last_data_field)
        else:
            result.extend(original_rounder(data))
    if empty_tail:
        result.extend(empty_tail)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Smartly rounding percentages in batch from a CSV file.'
    )
    parser.add_argument(
        'file_path',
        nargs='+',
        help='The path(s) of the target CSV file(s)'
    )
    args = parser.parse_args()
    for path in args.file_path:
        logging.info(f'Rounding the percentages in CSV file {path}...')
        csv_rounder(path)
