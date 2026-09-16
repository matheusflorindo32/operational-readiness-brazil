import hashlib
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from audit_xlsx_identity import (
    EXPECTED_SHEETS,
    MASTER,
    MASTER_SHA256,
    ROOT,
    fixed_timestamp_repack,
    scientific_invariants,
    semantic_representation,
    semantic_sha256,
)

CANONICAL = ROOT / "outputs/triage/2026-09-16/Operational_Readiness_Nonblocking_Queues.xlsx"
AUDIT_DIR = ROOT / "reporting/artifact_reconciliation/2026-09-16"
EXPECTED_SEMANTIC_SHA256 = "803e007a00129ee9ab5b361bc9a2c1ade1dc917554d2e9186d75f3f223953dc2"


class XlsxArtifactIdentityTest(unittest.TestCase):
    def test_zip_integrity_and_seven_sheet_structure(self):
        with zipfile.ZipFile(CANONICAL) as package:
            self.assertIsNone(package.testzip())
        document = semantic_representation(CANONICAL)
        self.assertEqual([sheet["name"] for sheet in document["sheets"]], EXPECTED_SHEETS)

    def test_scientific_invariants_and_master_evidence(self):
        checks = scientific_invariants(semantic_representation(CANONICAL))
        self.assertTrue(checks["all_pass"], checks)
        self.assertEqual(checks["master_sha256"], MASTER_SHA256)

    def test_semantic_hash_is_stable_under_zip_reserialization(self):
        expected = semantic_sha256(CANONICAL)
        with tempfile.TemporaryDirectory() as temp:
            repacked = Path(temp) / "repacked.xlsx"
            fixed_timestamp_repack(CANONICAL, repacked)
            with zipfile.ZipFile(repacked) as package:
                self.assertIsNone(package.testzip())
            self.assertNotEqual(hashlib.sha256(CANONICAL.read_bytes()).hexdigest(), hashlib.sha256(repacked.read_bytes()).hexdigest())
            self.assertEqual(semantic_sha256(repacked), expected)

    def test_recorded_semantic_hash(self):
        self.assertEqual(semantic_sha256(CANONICAL), EXPECTED_SEMANTIC_SHA256)

    def test_recorded_two_artifact_comparison_and_release_decision(self):
        comparison = json.loads((AUDIT_DIR / "semantic-comparison.json").read_text(encoding="utf-8"))
        cause = json.loads((AUDIT_DIR / "root-cause.json").read_text(encoding="utf-8"))
        self.assertTrue(comparison["semantic_equal"])
        self.assertEqual(comparison["artifact_a_semantic_sha256"], EXPECTED_SEMANTIC_SHA256)
        self.assertEqual(comparison["artifact_b_semantic_sha256"], EXPECTED_SEMANTIC_SHA256)
        self.assertTrue(comparison["artifact_a_invariants"]["all_pass"])
        self.assertTrue(comparison["artifact_b_invariants"]["all_pass"])
        self.assertEqual(cause["root_cause"], "ZIP_SERIALIZATION_DIFFERENCE")
        self.assertEqual(cause["release_decision"], "GO_WITH_DOCUMENTED_NONSEMANTIC_VARIANCE")


if __name__ == "__main__":
    unittest.main()
