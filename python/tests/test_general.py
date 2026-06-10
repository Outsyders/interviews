import importlib

import pytest


def load(rel_module):
    # General questions live in per-question folders, e.g.
    # general/q1_compress_string/main.py -> general.q1_compress_string.main
    return importlib.import_module(rel_module)


# --- q1: compress string ----------------------------------------------------
@pytest.mark.parametrize("raw,expected", [
    ("aaabbccccd", "a3b2c4d1"),
    ("a", "a1"),
    ("aabb", "a2b2"),
])
def test_compress_string(raw, expected):
    m = load("general.q1_compress_string.main")
    assert m.compress_string(raw) == expected


# --- q2: rotate matrix in place ---------------------------------------------
def test_rotate_matrix_in_place():
    m = load("general.q2_rotate_matrix.main")
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]
    result = m.rotate_matrix(matrix)
    assert result is None, "rotate_matrix should mutate in place, not return a new matrix"
    assert matrix == [
        [7, 4, 1],
        [8, 5, 2],
        [9, 6, 3],
    ]


# --- q3: LRU cache ----------------------------------------------------------
def test_lru_cache_eviction():
    m = load("general.q3_lru_cache.main")
    cache = m.LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1      # 1 is now most-recently-used
    cache.put(3, 3)               # capacity exceeded -> evict key 2
    assert cache.get(2) == -1
    cache.put(4, 4)               # evict key 1
    assert cache.get(1) == -1
    assert cache.get(3) == 3
    assert cache.get(4) == 4
