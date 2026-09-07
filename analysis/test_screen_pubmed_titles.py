"""Focused negative and boundary tests for the controlled screening rubric."""

import unittest

from screen_pubmed_titles import classify, integrity


def record(**overrides):
    base = {
        "pmid": "99999999",
        "title": "Example record",
        "abstract": "An abstract is available.",
        "publication_types": ["Journal Article"],
        "corrections": [],
    }
    base.update(overrides)
    return base


class ScreeningRulesTest(unittest.TestCase):
    def test_retracted_record_is_blocked(self):
        item = record(
            publication_types=["Retracted Publication"],
            corrections=[{"ref_type": "RetractionIn", "pmid": "1"}],
        )
        self.assertEqual(classify(item, {"families": ["A"]})[0], "BLOCKED_INTEGRITY")

    def test_direct_context_and_domain_are_retained(self):
        item = record(title="Police officer readiness and physical performance")
        self.assertEqual(classify(item, {"families": ["A"]})[0], "INCLUDE_FULL_TEXT")

    def test_unrelated_engineering_record_is_excluded(self):
        item = record(title="Tokamak semiconductor performance")
        self.assertEqual(classify(item, {"families": ["A"]})[0], "EXCLUDE_TITLE_ABSTRACT")

    def test_title_only_ambiguous_record_is_pending(self):
        item = record(title="Organizational study", abstract="")
        self.assertEqual(classify(item, {"families": ["A"]})[0], "PENDING_ADJUDICATION")

    def test_erratum_requires_review(self):
        item = record(corrections=[{"ref_type": "ErratumIn", "pmid": "2"}])
        self.assertEqual(integrity(item), ("Correction", "Pending", "REVIEW_CORRECTION"))


if __name__ == "__main__":
    unittest.main()
