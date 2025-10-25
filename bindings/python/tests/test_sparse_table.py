import pytest
from advanced_ds_playground import SparseTable

def test_sparse_table_min_basic():
    print("\n[TEST] SparseTable: Basic min queries")
    arr = [5, 2, 4, 7, 1, 3]
    st = SparseTable(arr)
    print(f"[INFO] Array: {arr}")
    
    print("[STEP] Querying range [0, 0]")
    assert st.query(0, 0) == 5
    print("[STEP] Querying range [0, 2]")
    assert st.query(0, 2) == 2
    print("[STEP] Querying range [1, 4]")
    assert st.query(1, 4) == 1
    print("[STEP] Querying range [4, 5]")
    assert st.query(4, 5) == 1
    print("[STEP] Querying range [5, 5]")
    assert st.query(5, 5) == 3
    print("[INFO] All basic queries successful.")

def test_invalid_queries():
    print("\n[TEST] SparseTable: Invalid queries")
    
    print("[STEP] Querying empty table")
    st_empty = SparseTable([])
    assert st_empty.query(0, 0) is None
    print("[INFO] Empty table query returned None as expected.")

    arr = [1, 2, 3]
    st = SparseTable(arr)
    print(f"[INFO] Array: {arr}")
    
    print("[STEP] Querying l > r (2, 1)")
    assert st.query(2, 1) is None
    print("[INFO] Inverted range query returned None as expected.")
    
    print("[STEP] Querying r out of bounds (0, 10)")
    assert st.query(0, 10) is None
    print("[INFO] Out-of-bounds query returned None as expected.")