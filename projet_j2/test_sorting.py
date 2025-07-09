import pytest
from sorting import bubble_sort, merge_sort, quick_sort

def test_bubble_sort():
    assert bubble_sort([3, 1, 4, 1, 5, 9, 2]) == [1, 1, 2, 3, 4, 5, 9]

def test_merge_sort():
    assert merge_sort([3, 1, 4, 1, 5, 9, 2]) == [1, 1, 2, 3, 4, 5, 9]

def test_quick_sort():
    assert quick_sort([3, 1, 4, 1, 5, 9, 2]) == [1, 1, 2, 3, 4, 5, 9]