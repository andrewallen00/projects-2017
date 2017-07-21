import unittest
from perfectsquare import is_perfect_square


class PerfectSquareTestCase(unittest.TestCase):
    """Tests for `perfectsquare.py`."""

    def test_is_sixteen_a_perfect_square(self):
        """Is 16 successfully determined to be a perfect square?"""
        self.assertTrue(is_perfect_square(16))

    def test_is_eight_not_a_perfect_square(self):
        self.assertFalse(is_perfect_square(8), msg='Eight is not a perfect square!')

    def test_negative_number(self):
        for index in range(-1, -10, -1):
            self.assertFalse(is_perfect_square(index), msg='{} should not be determined to be a perfect square'.format(index))

    def test_zero(self):
        self.assertTrue(is_perfect_square(0))

if __name__ == '__main__':
    unittest.main()
