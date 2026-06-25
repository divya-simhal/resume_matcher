import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from engine.heap import MinHeap, top_k_frequent


def test_minheap_pops_in_ascending_order():
    heap = MinHeap()
    for item in [(5, "e"), (1, "a"), (3, "c"), (2, "b"), (4, "d")]:
        heap.push(item)
    popped = [heap.pop() for _ in range(len(heap))]
    assert popped == sorted(popped)


def test_top_k_frequent_basic():
    counts = {"python": 10, "flask": 5, "docker": 8, "sql": 1, "git": 3}
    result = top_k_frequent(counts, k=3)
    words = [w for w, _ in result]
    assert words == ["python", "docker", "flask"]


def test_top_k_frequent_descending_order():
    counts = {"a": 1, "b": 5, "c": 3, "d": 9, "e": 2}
    result = top_k_frequent(counts, k=5)
    counts_only = [c for _, c in result]
    assert counts_only == sorted(counts_only, reverse=True)


def test_top_k_with_k_larger_than_input():
    counts = {"a": 1, "b": 2}
    result = top_k_frequent(counts, k=10)
    assert len(result) == 2


def test_top_k_with_empty_input():
    result = top_k_frequent({}, k=5)
    assert result == []
