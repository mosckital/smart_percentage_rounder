import pytest
from src.rounder import original_rounder, percentage_rounder

TEST_DATA = [
    # hand made data
    ([3330, 3330, 3330, 10],
     [33.3, 33.3, 33.3, 0.1],
     [34, 33, 33, 0]),
    ([16666, 16666, 16666, 16666, 16666, 16666],
     [16.666, 16.666, 16.666, 16.666, 16.666, 16.666],
     [17, 17, 17, 17, 16, 16]),
    ([33333, 33333, 33333],
     [33.333, 33.333, 33.333],
     [34, 33, 33]),
    ([13626332, 47989636, 9596008, 28788024],
     [13.626332, 47.989636, 9.596008, 28.788024],
     [14, 48, 9, 29]),
    ([5760, 11260, 11255, 5765, 15960],
     [11.52, 22.52, 22.51, 11.53, 31.92],
     [11, 23, 22, 12, 32]),
    # encountered data
    ([58, 97, 81, 11, 8],
     [22.75, 38.04, 31.76, 4.31, 3.14],
     [23, 38, 32, 4, 3]),
    ([66, 84, 80, 14, 9],
     [26.09, 33.20, 31.62, 5.53, 3.56],
     [26, 33, 32, 5, 4]),
    ([97, 80, 65, 12, 1],
     [38.04, 31.37, 25.49, 4.71, 0.39],
     [38, 31, 26, 5, 0]),
    ([69, 90, 75, 18, 1],
     [27.27, 35.57, 29.64, 7.11, 0.40],
     [27, 36, 30, 7, 0]),
    ([41, 73, 111, 18, 9],
     [16.27, 28.97, 44.05, 7.14, 3.57],
     [16, 29, 44, 7, 4]),
    ([29, 55, 130, 29, 9],
     [11.51, 21.83, 51.59, 11.51, 3.57],
     [11, 22, 52, 11, 4]),
]


class TestRounder:

    EPS = 0.01

    @pytest.mark.parametrize(
        'values, ref_results',
        [(orig, refs) for orig, _, refs in TEST_DATA]
    )
    def test_original_rounder(self, values, ref_results):
        assert sum(ref_results) == pytest.approx(100, self.EPS)
        assert original_rounder(values) == ref_results

    @pytest.mark.parametrize(
        'values, ref_results',
        [(pct, refs) for _, pct, refs in TEST_DATA]
    )
    def test_percentage_rounder(self, values, ref_results):
        assert sum(values) == pytest.approx(100, self.EPS)
        assert sum(ref_results) == pytest.approx(100, self.EPS)
        assert percentage_rounder(values) == ref_results
