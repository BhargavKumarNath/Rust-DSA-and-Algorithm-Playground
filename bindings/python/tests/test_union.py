import pytest
from advanced_ds_playground import UnionFind

def test_initialization():
    print("\n[TEST] Initialization")
    uf = UnionFind(10)
    print(f"Created UnionFind with {uf.count} elements")
    assert uf.count == 10

def test_union_and_connected():
    print("\n[TEST] Union and Connected Operations")
    uf = UnionFind(10)

    print("[STEP] Union(1, 2)")
    uf.union(1, 2)
    assert uf.connected(1, 2)
    assert not uf.connected(1, 3)
    assert uf.count == 9

    print("[STEP] Union(2, 3)")
    uf.union(2, 3)
    assert uf.connected(1, 3)
    assert uf.count == 8

    # Test unioning already connected items
    print("[STEP] Union already connected elements (1, 3)")
    assert not uf.union(1, 3)
    assert uf.count == 8

def test_find():
    print("\n[TEST] Find Operation")
    uf = UnionFind(5)
    uf.union(0, 1)
    uf.union(2, 3)
    uf.union(0, 4)

    # Sets are {0, 1, 4} and {2, 3}
    root_0 = uf.find(0)
    print(f"[INFO] Root of set containing 0 is {root_0}")
    assert uf.find(1) == root_0
    assert uf.find(4) == root_0

    root_2 = uf.find(2)
    print(f"[INFO] Root of set containing 2 is {root_2}")
    assert uf.find(3) == root_2
    assert root_0 != root_2

def test_edge_cases():
    print("\n[TEST] Edge Cases")
    uf = UnionFind(1)
    print(f"[INFO] Single element set count = {uf.count}")
    assert uf.count == 1
    assert uf.connected(0, 0)

    uf = UnionFind(0)
    print(f"[INFO] Empty set count = {uf.count}")
    assert uf.count == 0

def test_out_of_bounds():
    print("\n[TEST] Out-of-Bounds Handling")
    uf = UnionFind(10)

    print("[STEP] Testing union(5, 10)")
    with pytest.raises(IndexError, match="Index out of bounds"):
        uf.union(5, 10)
    
    print("[STEP] Testing find(10)")
    with pytest.raises(IndexError, match="Index out of bounds"):
        uf.find(10)

    print("[STEP] Testing connected(10, 1)")    
    with pytest.raises(IndexError, match="Index out of bounds"):
        uf.connected(10, 1)