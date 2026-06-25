import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from engine import ResumeDocument, JobDescriptionDocument, MatchEngine


def test_identical_documents_score_high():
    text = "Python developer skilled in Flask, Docker, and SQL."
    resume = ResumeDocument(text)
    job = JobDescriptionDocument(text)
    result = MatchEngine(resume, job).analyze()
    assert result["score"] > 90


def test_unrelated_documents_score_low():
    resume = ResumeDocument("Pastry chef skilled in laminated dough and chocolate tempering.")
    job = JobDescriptionDocument("Backend engineer with Kubernetes and Terraform experience.")
    result = MatchEngine(resume, job).analyze()
    assert result["score"] < 30


def test_missing_skill_is_detected():
    resume = ResumeDocument("Python developer skilled in Flask and SQL.")
    job = JobDescriptionDocument("Need a Python developer with Flask, SQL, and Kubernetes experience.")
    result = MatchEngine(resume, job).analyze()
    assert "kubernetes" in result["missing"]
    assert "python" in result["common"]


def test_document_role_polymorphism():
    resume = ResumeDocument("some text")
    job = JobDescriptionDocument("some text")
    assert resume.role() == "resume"
    assert job.role() == "job_description"


def test_document_len_matches_token_count():
    doc = ResumeDocument("Python Flask Docker SQL")
    assert len(doc) == len(doc.tokens)


def test_score_bounds():
    resume = ResumeDocument("Python Flask SQL Docker Git AWS Kubernetes Terraform")
    job = JobDescriptionDocument("Python Flask SQL Docker Git AWS Kubernetes Terraform")
    result = MatchEngine(resume, job).analyze()
    assert 0 <= result["score"] <= 100
    assert 0 <= result["skill_coverage"] <= 100
    assert 0 <= result["keyword_coverage"] <= 100
