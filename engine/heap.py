


class MinHeap:
    

    def __init__(self):
        self._data = []

    def __len__(self):
        return len(self._data)

    def peek(self):
        return self._data[0]

    def push(self, item):
        self._data.append(item)
        self._sift_up(len(self._data) - 1)

    def pop(self):
        last = len(self._data) - 1
        self._data[0], self._data[last] = self._data[last], self._data[0]
        item = self._data.pop()
        if self._data:
            self._sift_down(0)
        return item

    def _sift_up(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if self._data[i] < self._data[parent]:
                self._data[i], self._data[parent] = self._data[parent], self._data[i]
                i = parent
            else:
                break

    def _sift_down(self, i):
        n = len(self._data)
        while True:
            left, right = 2 * i + 1, 2 * i + 2
            smallest = i
            if left < n and self._data[left] < self._data[smallest]:
                smallest = left
            if right < n and self._data[right] < self._data[smallest]:
                smallest = right
            if smallest == i:
                break
            self._data[i], self._data[smallest] = self._data[smallest], self._data[i]
            i = smallest


def top_k_frequent(word_counts, k):
    """Return the k (word, count) pairs with the highest counts, ranked
    descending, in O(n log k) time using a size-bounded min-heap.

    word_counts: dict[str, int] — e.g. a Counter of token frequencies.
    """
    heap = MinHeap()
    for word, count in word_counts.items():
        if len(heap) < k:
            heap.push((count, word))
        elif count > heap.peek()[0]:
            heap.pop()
            heap.push((count, word))

    result = []
    while len(heap):
        count, word = heap.pop()
        result.append((word, count))
    result.reverse()  # heap pops smallest-first; we want largest-first
    return result
