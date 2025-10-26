import pytest
from advanced_ds_playground_bindings import Treap

def test_insert_contains_len_inorder():
    print("\n[TEST] Treap: Insert, contains, len, inorder")
    t = Treap()
    print(f"[INFO] Initial empty state: {t.is_empty()}")
    assert t.is_empty()
    
    print("[STEP] Inserting 5, 3, 7, 3 (duplicate)")
    t.insert(5)
    t.insert(3)
    t.insert(7)
    t.insert(3)  # duplicate
    
    print(f"[INFO] Not empty: {not t.is_empty()}, Length: {t.len()}")
    assert not t.is_empty()
    assert t.len() == 4
    
    print("[STEP] Checking contains (3, 5, 7, 42)...")
    assert t.contains(3)
    assert t.contains(5)
    assert t.contains(7)
    assert not t.contains(42)
    print("[INFO] Contains checks passed.")
    
    inorder = t.inorder_vec()
    expected = [3, 3, 5, 7]
    print(f"[INFO] Inorder result: {inorder}")
    print(f"[INFO] Expected:       {expected}")
    assert inorder == expected

def test_remove_and_duplicates():
    print("\n[TEST] Treap: Remove and duplicates")
    t = Treap()
    print("[STEP] Inserting 10, 10, 5, 15")
    t.insert(10)
    t.insert(10)
    t.insert(5)
    t.insert(15)
    
    print(f"[STEP] Removing first 10. Length before: {t.len()}")
    t.remove(10)
    print(f"[INFO] Contains 10: {t.contains(10)}, Length after: {t.len()}")
    assert t.contains(10)
    assert t.len() == 3
    
    print(f"[STEP] Removing second 10. Length before: {t.len()}")
    t.remove(10)
    print(f"[INFO] Contains 10: {t.contains(10)}, Length after: {t.len()}")
    assert not t.contains(10)
    assert t.len() == 2
    
    print("[STEP] Removing non-existent key 42")
    t.remove(42)
    assert t.len() == 2
    
    expected = [5, 15]
    print(f"[INFO] Final inorder: {t.inorder_vec()}, Expected: {expected}")
    assert t.inorder_vec() == expected

def test_mass_inserts_removes_stability():
    print("\n[TEST] Treap: Mass inserts and removes")
    t = Treap()
    
    print("[STEP] Inserting 0..99")
    for v in range(100):
        t.insert(v)
    print(f"[INFO] Length after inserts: {t.len()}")
    assert t.len() == 100
    
    print("[STEP] Checking contains 0..99")
    for v in range(100):
        assert t.contains(v)
    print("[INFO] All 100 elements found.")
        
    print("[STEP] Removing 0..99")
    for v in range(100):
        t.remove(v)
        
    print(f"[INFO] Final empty state: {t.is_empty()}, Length: {t.len()}")
    assert t.is_empty()