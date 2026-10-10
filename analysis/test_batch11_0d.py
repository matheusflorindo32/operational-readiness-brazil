from pathlib import Path
import csv
import hashlib
import json

OUTPUT = Path("batch11_0d")


def rows(name):
    with (OUTPUT / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def canonical_hash(path):
    raw = path.read_bytes()
    if path.suffix.lower() in {".csv", ".json", ".md"}:
        raw = raw.replace(b"\r\n", b"\n")
    return hashlib.sha256(raw).hexdigest()


manifest = json.loads((OUTPUT / "BATCH11_0D_MANIFEST.json").read_text(encoding="utf-8"))
integrity = rows("EXTERNAL_INTEGRITY_RECHECK_26.csv")
assert len(integrity) == 26
assert {row["Final_Integrity_Status"] for row in integrity} == {"INTEGRITY_CLEAR"}
assert all(row["PMID_Status"] == "PMID_CONFIRMED_BY_PUBMED" for row in integrity)
assert all(row["Duplicate_Status"] == "NO_DUPLICATE_PUBLICATION_IDENTIFIED" for row in integrity)
claims = rows("CLAIM_READY_CANDIDATE_LEDGER.csv")
assert len(claims) == 12
assert all(row["CLAIM_READY_CANDIDATE"] == "YES" and row["Claim_Ready"] == "NO" for row in claims)
assert len(rows("CONTEXTUAL_INTEGRITY_STATUS.csv")) == 12
assert len(rows("INTEGRITY_HUMAN_REVIEW_QUEUE.csv")) == 0
assert rows("BRAZIL_EXPANSION_STATUS_POST_INTEGRITY.csv")[0]["Brazil_Direct_Inflation"] == "0"
assert rows("INTERNATIONAL_POST_INTEGRITY_VIABILITY.csv")[0]["Next_Gate"] == "GO_FULL_MANUSCRIPT_RECONSTRUCTION"
assert manifest["integrity_guards"]["EV-1379"].startswith("CANONICAL_BLOCKED")
assert "support use 0" in manifest["integrity_guards"]["EV-0052_EV-0140_EV-1066"]
for name, expected in manifest["artifact_sha256"].items():
    assert canonical_hash(OUTPUT / name) == expected, name
print("BATCH11_0D tests PASS", len(integrity), len(claims))
