

from abc import ABC, abstractmethod
from collections import Counter

from .tokenizer import Tokenizer


class Document(ABC):
    def __init__(self, raw_text):
        self.raw_text = raw_text
        self.tokens = Tokenizer.tokenize(raw_text)
        self.word_counts = Counter(self.tokens)     # hash map: word -> frequency
        self.token_set = set(self.tokens)            # hash set: O(1) membership checks

    @abstractmethod
    def role(self):
        raise NotImplementedError

    def __len__(self):
        return len(self.tokens)

    def __repr__(self):
        return f"<{self.__class__.__name__} tokens={len(self.tokens)}>"


class ResumeDocument(Document):
    def role(self):
        return "resume"


class JobDescriptionDocument(Document):
    def role(self):
        return "job_description"
