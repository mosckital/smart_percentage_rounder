import csv
import pytest
from os.path import join, dirname
from src.rounder import original_rounder, percentage_rounder


def read_test_data(csv_path):
    """
    To read the test data from a CSV file. This CSV file should only contain
    data and no other value.

    :param csv_path: the path to the CSV file
    :return: the read data in a two dimension array
    """
    with open(csv_path, newline='') as f:
        reader = csv.reader(f)
        return [[float(v) for v in row] for row in reader]


SCRIPT_PATH = dirname(__file__)
INPUT_ORIGINAL_PATH = join(SCRIPT_PATH, './test_files/test_input_original.csv')
INPUT_PERCENTAGE_PATH = join(SCRIPT_PATH, './test_files/test_input_percentage.csv')
OUTPUT_EXPECTED_PATH = join(SCRIPT_PATH, './test_files/test_output_expected.csv')


class TestRounder:
    """Test suite for the methods in the module `src/rounder.py`."""

    EPS = 0.01  # epsilon for float comparison
    GOAL = 1.00  # target (100%) in decimal
    PERCENTAGE_GOAL = 100.0  # target (100%) in percentage unit

    @pytest.mark.parametrize(
        'values, ref_results',
        list(zip(
            read_test_data(INPUT_ORIGINAL_PATH),
            read_test_data(OUTPUT_EXPECTED_PATH),
        )),
    )
    def test_original_rounder(self, values, ref_results):
        """Test case for the method `original_rounder()`."""
        assert sum(ref_results) == pytest.approx(self.GOAL, self.EPS), \
            "The expected results should sum to 100%"
        assert original_rounder(values) == ref_results, \
            "The calculated results should equal to expected ones"

    @pytest.mark.parametrize(
        'values, ref_results',
        list(zip(
            read_test_data(INPUT_PERCENTAGE_PATH),
            read_test_data(OUTPUT_EXPECTED_PATH),
        )),
    )
    def test_percentage_rounder(self, values, ref_results):
        """Test case for the method `percentage_rounder()`."""
        assert sum(values) == pytest.approx(self.PERCENTAGE_GOAL, self.EPS), \
            "The input percentages should sum to 100%"
        assert sum(ref_results) == pytest.approx(self.GOAL, self.EPS), \
            "The expected results should sum to 100%"
        assert percentage_rounder(values) == ref_results, \
            "The calculated results should equal to expected ones"
