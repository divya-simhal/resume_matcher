

from .document import Document
from .heap import top_k_frequent
from .skills import build_skill_trie

_SKILL_TRIE = build_skill_trie()  # built once, shared across requests


class MatchEngine:
    def __init__(self, resume: Document, job: Document, top_k: int = 30):
        self.resume = resume
        self.job = job
        self.top_k = top_k

    def _skill_analysis(self):
        resume_skills = _SKILL_TRIE.extract_phrases(self.resume.tokens)
        job_skills = _SKILL_TRIE.extract_phrases(self.job.tokens)

        matched = job_skills & resume_skills       # set intersection
        missing = job_skills - resume_skills        # set difference
        coverage = (len(matched) / len(job_skills) * 100) if job_skills else 0.0

        return sorted(matched), sorted(missing), coverage

    def _keyword_analysis(self, exclude_words):
        filtered_counts = {
            w: c for w, c in self.job.word_counts.items() if w not in exclude_words
        }
        top_job_words = top_k_frequent(filtered_counts, self.top_k)

        matched, missing = [], []
        for word, _count in top_job_words:
            (matched if word in self.resume.token_set else missing).append(word)

        coverage = (len(matched) / len(top_job_words) * 100) if top_job_words else 0.0
        return matched, missing, coverage

    def analyze(self):
        skill_matched, skill_missing, skill_coverage = self._skill_analysis()

        exclude = set()
        for phrase in (*skill_matched, *skill_missing):
            exclude.update(phrase.split())

        kw_matched, kw_missing, kw_coverage = self._keyword_analysis(exclude)

        # Skills matter more to an ATS filter than generic word overlap.
        score = round(0.65 * skill_coverage + 0.35 * kw_coverage, 1)

        return {
            "score": score,
            "skill_coverage": round(skill_coverage, 1),
            "keyword_coverage": round(kw_coverage, 1),
            "common": skill_matched + kw_matched,
            "missing": skill_missing + kw_missing,
            "resume_word_count": len(self.resume),
            "job_word_count": len(self.job),
        }
