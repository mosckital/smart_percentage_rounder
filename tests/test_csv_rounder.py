import csv
import pytest
from tempfile import TemporaryDirectory as TmpDir
from shutil import copy
from os.path import join, dirname
from rounders.csv_rounder import csv_rounder


SCRIPT_PATH = dirname(__file__)
DATA_NO_TOTAL_PATH = join(SCRIPT_PATH, './test_files/test_data_no_total.csv')
RESULT_NO_TOTAL_PATH = join(SCRIPT_PATH, './test_files/test_result_no_total.csv')
DATA_WITH_TOTAL_PATH = join(SCRIPT_PATH, './test_files/test_data_with_total.csv')
RESULT_WITH_TOTAL_PATH = join(SCRIPT_PATH, './test_files/test_result_with_total.csv')


class TestCsvRounder:
    """Test suite for the methods in the module `rounders/csv_rounder.py`."""

    @pytest.mark.parametrize('input_path, answer_path, has_total_col', [
        (DATA_NO_TOTAL_PATH,
         RESULT_NO_TOTAL_PATH,
         False),
        (DATA_WITH_TOTAL_PATH,
         RESULT_WITH_TOTAL_PATH,
         True),
    ])
    def test_csv_rounder(self, input_path, answer_path, has_total_col):
        """Test case for the method `csv_rounder()`."""
        with TmpDir() as tmp_dir:
            # generate the output file in a temporary directory
            tmp_input_path = copy(input_path, tmp_dir)
            tmp_output_path = csv_rounder(tmp_input_path, has_total_col)
            # compare output file and answer file one line by one line
            with open(tmp_output_path, newline='') as output, \
                    open(answer_path, newline='') as answer:
                output_reader = csv.reader(output)
                answer_reader = csv.reader(answer)
                for o, a in zip(output_reader, answer_reader):
                    assert o == a
