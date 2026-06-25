import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from engine.trie import Trie


def test_single_word_match():
    trie = Trie()
    trie.insert("python")
    found = trie.extract_phrases(["i", "love", "python", "code"])
    assert found == {"python"}


def test_multi_word_phrase_match():
    trie = Trie()
    trie.insert("machine learning")
    tokens = ["skilled", "in", "machine", "learning", "models"]
    found = trie.extract_phrases(tokens)
    assert found == {"machine learning"}


def test_greedy_longest_match():
    trie = Trie()
    trie.insert("machine")
    trie.insert("machine learning")
    tokens = ["machine", "learning", "expert"]
    found = trie.extract_phrases(tokens)
    # should prefer the longer phrase, not match "machine" and stop short
    assert found == {"machine learning"}


def test_no_match_returns_empty_set():
    trie = Trie()
    trie.insert("python")
    found = trie.extract_phrases(["javascript", "react", "css"])
    assert found == set()


def test_multiple_distinct_phrases():
    trie = Trie()
    for phrase in ["python", "rest api", "ci cd"]:
        trie.insert(phrase)
    tokens = ["python", "developer", "with", "rest", "api", "and", "ci", "cd"]
    found = trie.extract_phrases(tokens)
    assert found == {"python", "rest api", "ci cd"}
