# ScanMatch — Resume/JD Matcher (OOP + DSA Edition)

A Flask web app that scores resume ↔ job description compatibility and
runs an automated keyword gap analysis — built entirely on hand-rolled
data structures and OOP design, **no ML/NLP libraries**.

Built on top of a CLI prototype, rewritten as a structured engine to
practice and demonstrate core CS fundamentals: a Trie, a binary heap,
hash maps/sets, and an abstract-class-based OOP hierarchy.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/flask-3.0-black)
![No ML deps](https://img.shields.io/badge/dependencies-0%20ML%20libs-success)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## Why this version

The matching logic is implemented from scratch using classic data
structures instead of a library like scikit-learn — so every part of
the scoring pipeline is something you can explain line-by-line in an
interview, with real Big-O reasoning behind each design choice.

## Data structures & OOP concepts used

| Concept | Where | Why |
|---|---|---|
| **Trie (prefix tree)** | `engine/trie.py` | Detects multi-word skill phrases ("machine learning", "rest api") in a single left-to-right scan, independent of how many skills are in the dictionary |
| **Binary min-heap (hand-rolled, no `heapq`)** | `engine/heap.py` | Solves the classic *Top-K Frequent Elements* problem — finds the K most important JD keywords in `O(n log k)` instead of fully sorting in `O(n log n)` |
| **Hash map / hash set** | `engine/document.py` | `Counter` for word frequency, `set` for `O(1)` average membership checks and `O(min(a,b))` intersection/difference |
| **Abstract base class** | `engine/document.py` | `Document(ABC)` defines the shared contract; `ResumeDocument` / `JobDescriptionDocument` only override `role()` |
| **Inheritance + polymorphism** | `engine/document.py` | Both subclasses share 100% of the tokenizing/counting logic; only their identity differs |
| **Composition** | `engine/match_engine.py` | `MatchEngine` is composed of two `Document` instances + the shared `Trie`, rather than the documents knowing how to compare themselves |

## How the pipeline works

1. **Tokenize** — lowercase, strip punctuation, drop stopwords (`engine/tokenizer.py`)
2. **Build documents** — `ResumeDocument` / `JobDescriptionDocument` each
   build a token list, a `Counter` (hash map), and a `set` (hash set) on construction
3. **Skill detection** — `MatchEngine` runs both documents' tokens through
   the shared `Trie` to extract known skill phrases in one linear pass each;
   `matched = job_skills & resume_skills`, `missing = job_skills - resume_skills`
4. **Keyword ranking** — the job description's remaining (non-skill) words
   are ranked by frequency using a size-K min-heap (`top_k_frequent`),
   instead of sorting the entire vocabulary
5. **Score blend** — `0.65 * skill_coverage + 0.35 * keyword_coverage`
   (named skills matter more to an ATS filter than generic word overlap)

## Project structure

```
resume-matcher-dsa/
├── app.py                      # Flask routes, file upload handling
├── engine/
│   ├── trie.py                  # Trie — multi-word skill detection
│   ├── heap.py                  # Hand-rolled min-heap — Top-K Frequent pattern
│   ├── tokenizer.py             # Text cleanup
│   ├── skills.py                # Curated skill vocabulary
│   ├── document.py              # Abstract Document + ResumeDocument / JobDescriptionDocument
│   └── match_engine.py          # Orchestrates Trie + Heap + set ops → final score
├── tests/
│   ├── test_trie.py
│   ├── test_heap.py
│   └── test_match_engine.py
├── templates/index.html
├── static/{css,js}/
└── requirements.txt              # Flask, PyPDF2, python-docx — that's it
```

## Getting started

```bash
git clone https://github.com/<your-username>/resume-matcher-dsa.git
cd resume-matcher-dsa
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open **http://127.0.0.1:5000**.

## Testing

```bash
pip install pytest
python -m pytest tests/ -v
```

16 tests covering the Trie (greedy longest-match, multi-phrase detection),
the heap (ordering, top-K correctness, edge cases), and the engine
(scoring bounds, polymorphism, gap detection).

## API

### `POST /api/analyze`

**Request:** `multipart/form-data` with `resume` and `job_description`
files (`.pdf`, `.docx`, or `.txt`).

**Response:**
```json
{
  "score": 69.5,
  "skill_coverage": 80.0,
  "keyword_coverage": 50.0,
  "common": ["ci cd", "docker", "flask", "machine learning", "python"],
  "missing": ["kubernetes", "terraform"],
  "resume_word_count": 18,
  "job_word_count": 15
}
```

## Roadmap / ideas for next iteration

- [ ] Expand the skill dictionary, or load it from a config file
- [ ] Add a Binary Search Tree variant of the skill index and benchmark
      it against the Trie for comparison
- [ ] LRU cache for repeated resume/JD pairs
- [ ] Section-aware parsing (skills section weighted higher than prose)

## License

MIT
