"""Regression checks for structural parsing; synthetic records only."""

import tempfile
import unittest
from pathlib import Path

from audit_pubmed_structure import bib_records, duplicates, normalize_title, ris_records


class BibliographicParserTests(unittest.TestCase):
    def parse(self, content, parser):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.txt"
            path.write_text(content, encoding="utf-8")
            return parser(path)

    def test_ris_repeated_fields_and_multiline(self):
        rows = self.parse(
            "TY  - JOUR\nTI  - Synthetic\n continued\nAU  - Alpha\nAU  - Beta\nER  - \n",
            ris_records,
        )
        self.assertEqual(rows[0]["TI"], ["Synthetic continued"])
        self.assertEqual(rows[0]["AU"], ["Alpha", "Beta"])

    def test_ris_incomplete_and_nested_records_rejected(self):
        for text in (
            "TY  - JOUR\nTI  - Incomplete\n",
            "TY  - JOUR\nTY  - JOUR\nER  - \n",
        ):
            with self.subTest(text=text), self.assertRaises(AssertionError):
                self.parse(text, ris_records)

    def test_bibtex_balanced_and_escaped_braces(self):
        rows = self.parse(
            "@article{synthetic,\n title = {{Nested} and \\{literal\\}},\n year = {2020},\n}\n",
            bib_records,
        )
        self.assertEqual(rows[0]["title"], "{Nested} and \\{literal\\}")
        self.assertEqual(rows[0]["year"], "2020")

    def test_bibtex_incomplete_rejected(self):
        with self.assertRaises(AssertionError):
            self.parse("@article{synthetic,\n title = {unclosed\n", bib_records)

    def test_missing_doi_is_not_duplicate(self):
        self.assertEqual(
            duplicates([{"doi": "", "pmid": "1"}, {"doi": "", "pmid": "2"}], "doi"), {}
        )
        self.assertEqual(
            duplicates(
                [
                    {"doi": "10.0000/test", "pmid": "1"},
                    {"doi": "10.0000/test", "pmid": "2"},
                ],
                "doi",
            ),
            {"10.0000/test": ["1", "2"]},
        )

    def test_title_normalization_retains_distinctions(self):
        self.assertEqual(normalize_title(" {Synthetic}   TITLE. "), "synthetic title")
        self.assertNotEqual(
            normalize_title("Synthetic title 1"), normalize_title("Synthetic title 2")
        )


if __name__ == "__main__":
    unittest.main()
