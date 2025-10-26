import pytest
from advanced_ds_playground_bindings import FenwickTree

def test_init_from_size():
    print("\n[TEST] FenwickTree: Initialization from size")
    ft = FenwickTree(10)
    print(f"[INFO] Initialized with size 10. Length: {len(ft)}")
    assert len(ft) == 10
    assert ft.query(9) == 0

def test_init_from_list():
    print("\n[TEST] FenwickTree: Initialization from list")
    values = [1, 2, 3, 4, 5]
    ft = FenwickTree(values)
    print(f"[INFO] Initialized from list: {values}. Length: {len(ft)}")
    print("[INFO] Querying prefix sums...")
    assert len(ft) == 5
    assert ft.query(0) == 1
    assert ft.query(2) == 6  
    assert ft.query(4) == 15 
    print("[INFO] Prefix sums match expected.")

def test_invalid_init():
    print("\n[TEST] FenwickTree: Invalid initialization (string)")
    with pytest.raises(ValueError):
        FenwickTree("invalid input")
    print("[INFO] Correctly raised ValueError.")

def test_add_and_query():
    print("\n[TEST] FenwickTree: Add and query")
    ft = FenwickTree(10)
    
    print("[STEP] Add 100 at index 5")
    ft.add(5, 100)
    assert ft.query(4) == 0
    assert ft.query(5) == 100
    assert ft.query(9) == 100
    print("[INFO] Queries after first add are correct.")

    print("[STEP] Add -20 at index 5")
    ft.add(5, -20)
    assert ft.query(5) == 80
    print("[INFO] Query after delta update is correct.")

    print("[STEP] Add 10 at index 2")
    ft.add(2, 10)
    assert ft.query(2) == 10
    assert ft.query(4) == 10
    assert ft.query(5) == 90 
    print("[INFO] Queries after second add are correct.")

def test_range_sum():
    print("\n[TEST] FenwickTree: Range sum")
    values = [1, 1, 2, 2, 3, 3, 4, 4]
    ft = FenwickTree(values)
    print(f"[INFO] Initialized from list: {values}")
    
    assert ft.range_sum(0, 7) == 20
    print("[INFO] Range (0, 7) sum correct.")
    assert ft.range_sum(2, 5) == 10 
    print("[INFO] Range (2, 5) sum correct.")
    assert ft.range_sum(4, 4) == 3
    print("[INFO] Single-element range (4, 4) sum correct.")
    assert ft.range_sum(7, 0) == 0 
    print("[INFO] Inverted range (7, 0) sum correct.")

def test_out_of_bounds():
    print("\n[TEST] FenwickTree: Out-of-bounds handling")
    ft = FenwickTree(10)
    
    print("[STEP] Testing add(10)")
    with pytest.raises(IndexError):
        ft.add(10, 1)
        
    print("[STEP] Testing query(10)")
    with pytest.raises(IndexError):
        ft.query(10)
        
    print("[STEP] Testing range_sum(0, 10)")
    with pytest.raises(IndexError):
        ft.range_sum(0, 10)
        
    print("[INFO] Out-of-bounds checks passed.")
    assert ft.range_sum(10, 9) == 0