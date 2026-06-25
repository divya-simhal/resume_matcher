


class TrieNode:
    __slots__ = ("children", "is_end")

    def __init__(self):
        self.children = {}   # word -> TrieNode
        self.is_end = False  # True if a skill phrase ends at this node


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, phrase):
        """Insert a (possibly multi-word) skill phrase, e.g. 'machine learning'."""
        node = self.root
        for word in phrase.split():
            node = node.children.setdefault(word, TrieNode())
        node.is_end = True

    def match_at(self, tokens, start):
        """Try to match the *longest* skill phrase starting at tokens[start].

        Returns (phrase, end_index) if a match was found, where end_index
        is the index just past the matched tokens — or (None, start) if
        nothing matched.
        """
        node = self.root
        i = start
        matched_words = []
        best_phrase, best_end = None, start

        while i < len(tokens) and tokens[i] in node.children:
            node = node.children[tokens[i]]
            matched_words.append(tokens[i])
            i += 1
            if node.is_end:
                # Keep extending greedily — "machine" alone shouldn't win
                # over "machine learning" if both are valid skills.
                best_phrase = " ".join(matched_words)
                best_end = i

        return best_phrase, best_end

    def extract_phrases(self, tokens):
        """Single left-to-right scan over the token list, greedily matching
        the longest skill phrase at each position. O(n) scan where each
        token is visited at most once thanks to the index jump on a match.
        """
        found = set()
        i = 0
        n = len(tokens)
        while i < n:
            phrase, end = self.match_at(tokens, i)
            if phrase:
                found.add(phrase)
                i = end  # jump past the matched phrase
            else:
                i += 1
        return found
