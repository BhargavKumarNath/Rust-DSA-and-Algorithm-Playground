import pytest
from advanced_ds_playground import UnionFind

def test_initialization():
    uf = UnionFind(10)
    assert uf.count == 10

def test_union_and_connected():
    uf = UnionFind(10)
    uf.union(1, 2)
    assert uf.connected(1, 2)
    assert not uf.connected(1, 3)
    assert uf.count == 9

    uf.union(2, 3)
    assert uf.connected(1, 3)
    assert uf.count == 8

    # Test unioning already connected items
    assert not uf.union(1, 3)
    assert uf.count == 8

def test_find():
    uf = UnionFind(5)
    uf.union(0, 1)
    uf.union(2, 3)
    uf.union(0, 4)

    # Sets are {0, 1, 4} and {2, 3}
    root_0 = uf.find(0)
    assert uf.find(1) == root_0
    assert uf.find(4) == root_0

    root_2 = uf.find(2)
    assert uf.find(3) == root_2
    assert root_0 != root_2

def test_edge_cases():
    uf = UnionFind(1)
    assert uf.count == 1
    assert uf.connected(0, 0)

    uf = UnionFind(0)
    assert uf.count == 0

def test_out_of_bounds():
    uf = UnionFind(10)
    with pytest.raises(IndexError, match="Index out of bounds"):
        uf.union(5, 10)
    with pytest.raises(IndexError, match="Index out of bounds"):
        uf.find(10)
    with pytest.raises(IndexError, match="Index out of bounds"):
        uf.connected(10, 1)