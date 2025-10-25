import pytest
from advanced_ds_playground import FenwickTree

def test_init_from_size():
    ft = FenwickTree(10)
    assert len(ft) == 10
    assert ft.query(9) == 0

def test_init_from_list():
    values = [1, 2, 3, 4, 5]
    ft = FenwickTree(values)
    assert len(ft) == 5
    assert ft.query(0) == 1
    assert ft.query(2) == 6  
    assert ft.query(4) == 15 

def test_invalid_init():
    with pytest.raises(ValueError):
        FenwickTree("invalid input")

def test_add_and_query():
    ft = FenwickTree(10)
    ft.add(5, 100)
    assert ft.query(4) == 0
    assert ft.query(5) == 100
    assert ft.query(9) == 100

    ft.add(5, -20)
    assert ft.query(5) == 80

    ft.add(2, 10)
    assert ft.query(2) == 10
    assert ft.query(4) == 10
    assert ft.query(5) == 90 

def test_range_sum():
    values = [1, 1, 2, 2, 3, 3, 4, 4]
    ft = FenwickTree(values)
    assert ft.range_sum(0, 7) == 20
    assert ft.range_sum(2, 5) == 10 
    assert ft.range_sum(4, 4) == 3
    assert ft.range_sum(7, 0) == 0 

def test_out_of_bounds():
    ft = FenwickTree(10)
    with pytest.raises(IndexError):
        ft.add(10, 1)
    with pytest.raises(IndexError):
        ft.query(10)
    with pytest.raises(IndexError):
        ft.range_sum(0, 10)
    assert ft.range_sum(10, 9) == 0