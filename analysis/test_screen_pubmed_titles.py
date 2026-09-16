"""Focused negative and boundary tests for the controlled screening rubric."""

import unittest
import xml.etree.ElementTree as ET

from refresh_pubmed_screening import parse_book
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
    def test_pubmed_book_parser_preserves_collective_authors_collection_and_doi(self):
        article = ET.fromstring(
            """
            <PubmedBookArticle>
              <BookDocument>
                <PMID>25121201</PMID>
                <ArticleIdList><ArticleId IdType="bookaccession">NBK232892</ArticleId><ArticleId IdType="doi">10.17226/5257</ArticleId></ArticleIdList>
                <Book>
                  <Publisher><PublisherName>National Academies Press (US)</PublisherName></Publisher>
                  <BookTitle>Book title</BookTitle>
                  <CollectionTitle>Series title</CollectionTitle>
                  <PubDate><Year>1996</Year></PubDate>
                  <AuthorList><Author><CollectiveName>Committee name</CollectiveName></Author></AuthorList>
                  <ELocationID EIdType="doi">10.17226/5257</ELocationID>
                </Book>
                <PublicationType>Review</PublicationType>
              </BookDocument>
              <PubmedBookData><PublicationStatus>ppublish</PublicationStatus></PubmedBookData>
            </PubmedBookArticle>
            """
        )
        parsed = parse_book(article)
        self.assertEqual(parsed["doi"], "10.17226/5257")
        self.assertEqual(parsed["authors"], ["Committee name"])
        self.assertEqual(parsed["journal"], "Series title")

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
