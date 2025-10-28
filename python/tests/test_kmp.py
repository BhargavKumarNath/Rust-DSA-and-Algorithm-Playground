import pytest
from advanced_ds_playground_bindings import find_all, prefix_function

def test_prefix_function_basic():
    print("\n[TEST] KMP: Prefix function basic")
    p = "ababcabab"
    pi = prefix_function(p)
    expected = [0, 0, 1, 2, 0, 1, 2, 3, 4] 
    print(f"[INFO] Pattern: '{p}'")
    print(f"[INFO] Got pi:    {pi}")
    print(f"[INFO] Expected:  {expected}")
    assert pi == expected

def test_find_all_simple():
    print("\n[TEST] KMP: Find all simple")
    text = "ababcabababc"
    pattern = "abab"
    occ = find_all(text, pattern)
    expected = [0, 5, 7] 
    print(f"[INFO] Text:    '{text}'")
    print(f"[INFO] Pattern: '{pattern}'")
    print(f"[INFO] Got occurrences: {occ}")
    print(f"[INFO] Expected:        {expected}")
    assert occ == expected

def test_find_all_no_match():
    print("\n[TEST] KMP: Find all no match")
    text = "hello world"
    pattern = "abc"
    occ = find_all(text, pattern)
    print(f"[INFO] Text: '{text}', Pattern: '{pattern}', Occurrences: {occ}")
    assert occ == []

def test_find_all_overlapping():
    print("\n[TEST] KMP: Find all overlapping")
    text = "aaaaa"
    pattern = "aa"
    occ = find_all(text, pattern)
    expected = [0, 1, 2, 3]
    print(f"[INFO] Text: '{text}', Pattern: '{pattern}'")
    print(f"[INFO] Got occurrences: {occ}, Expected: {expected}")
    assert occ == expected

def test_empty_pattern():
    print("\n[TEST] KMP: Empty pattern")
    occ = find_all("anytext", "")
    print(f"[INFO] Got occurrences: {occ}")
    assert occ == []

def test_pattern_longer_than_text():
    print("\n[TEST] KMP: Pattern longer than text")
    occ = find_all("abc", "abcdef")
    print(f"[INFO] Got occurrences: {occ}")
    assert occ == []