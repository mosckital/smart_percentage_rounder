"""
This script provides methods to smartly round a list of percentages, which sum
to 100%, to percentages having no decimal, and guarantees that the sum of the
rounded percentages is always 100%.

In contrast, simply applying `round()` to the list of percentages may lead the
sum of the rounded percentages to 99%, 101% or even less accurate result.

The implementation is based on the
[Largest Remainder Method](https://en.wikipedia.org/wiki/Largest_remainder_method).
"""
import argparse
from math import floor
from operator import itemgetter
from typing import Sequence, Union


Number = Union[int, float]
"""Type alias for the numbers."""
hundred = 100
"""To replace 100 in codes."""


def original_rounder(values: Sequence[Number]) -> Sequence[Number]:
    """
    To convert a list of original data to percentages and then smartly round the
    percentages to no decimal with a guarantee that the sum of rounded
    percentages is 100%.

    :param values: the list of original data
    :return: the list of rounded percentage
    """
    _sum = sum(values)
    return percentage_rounder(list(map(lambda v: 100 * v / _sum, values)))


def percentage_rounder(values: Sequence[Number]) -> Sequence[Number]:
    """
    To smartly round a list of percentages to decimal so that the sum of the
    rounded values is guaranteed 100%.

    :param values: the list of input percentages
    :return: the list of rounded percentages
    """
    # round down all percentages to no decimal
    round_downs = list(map(floor, values))
    down_sum = sum(round_downs)
    if down_sum == hundred:
        return round_downs
    # sort the residuals from high to low
    residuals = [v - rd for v, rd in zip(values, round_downs)]
    residuals_with_round_downs = list(zip(range(len(residuals)), residuals, round_downs))
    sorted_residuals = sorted(residuals_with_round_downs, key=itemgetter(1, 2), reverse=True)
    idx = 0
    # allocate the remaining points in the sorted order until 100% is achieved
    while down_sum < hundred:
        round_downs[sorted_residuals[idx][0]] += 1
        idx += 1
        down_sum += 1
    return [v / 100 for v in round_downs]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Smart rounder which guarantees the sum of rounded percentages is 100%'
    )
    parser.add_argument(
        '-p', '--percentage',
        action='store_const',
        const=True,
        default=False,
        help='Flag that the input will be a list of percentages instead of original values.'
    )
    parser.add_argument(
        'values',
        nargs='+',
        help='The original values (or the percentages if -p is flagged) to calculate smartly rounded percentages.'
    )
    args = parser.parse_args()
    rounder = percentage_rounder if args.percentage else original_rounder
    listed_values = list(map(float, args.values))
    results = rounder(listed_values)
    results_str = ' '.join(map(str, results))
    print('Smartly rounded percentages:')
    print(f'{results_str}')
