import argparse
from math import floor
from operator import itemgetter
from typing import Sequence, Union


Number = Union[int, float]
hundred = 100


def original_rounder(values: Sequence[Number]) -> Sequence[Number]:
    _sum = sum(values)
    return percentage_rounder(list(map(lambda v: 100 * v / _sum, values)))


def percentage_rounder(values: Sequence[Number]) -> Sequence[Number]:
    round_downs = list(map(floor, values))
    down_sum = sum(round_downs)
    if down_sum == hundred:
        return round_downs
    residuals = [v - rd for v, rd in zip(values, round_downs)]
    residuals_with_round_downs = list(zip(range(len(residuals)), residuals, round_downs))
    sorted_residuals = sorted(residuals_with_round_downs, key=itemgetter(1, 2), reverse=True)
    idx = 0
    while down_sum < hundred:
        round_downs[sorted_residuals[idx][0]] += 1
        idx += 1
        down_sum += 1
    return round_downs


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
