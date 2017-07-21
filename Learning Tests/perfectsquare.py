import math


def is_perfect_square(number):
    """Return True if the *number* is a perfect square"""
    if number < 0:
        return False
    square_root = math.sqrt(number)
    if square_root - round(square_root) == 0:
        return True
    else:
        return False
