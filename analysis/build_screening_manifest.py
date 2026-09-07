"""Create a compact integrity manifest for the controlled screening run."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def file_record(path: Path, base: Path):
    return {
        "path": path.relative_to(base).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--backup-root", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    committed = [
        "outputs/8a39e3c813da/PREMIUM_ELITE_DIAMANTE_Evidence_Command_Center.xlsx",
        "reporting/screening/2026-09-07/screening-decision-ledger.csv",
        "reporting/screening/2026-09-07/screening-summary.json",
        "reporting/screening/2026-09-07/screening-exceptions.json",
        "reporting/screening/2026-09-07/workbook-functional-tests.json",
        "reporting/screening/2026-09-07/precheck/audit.json",
        "reporting/screening/2026-09-07/postcheck/audit.json",
    ]
    payload = {
        "run_date": "2026-09-07",
        "reference_commit": "ae25ad9054193f8ac3be82061f6fe7906d989ec9",
        "backup_root": str(args.backup_root.resolve()),
        "external_files": [
            file_record(path, args.backup_root)
            for path in sorted(args.backup_root.rglob("*"))
            if path.is_file()
        ],
        "repository_files": [
            file_record(args.repo_root / relative, args.repo_root) for relative in committed
        ],
        "drive": {
            "canonical_google_sheet_id": "1X6MerTU2oZYup6LMI0SVBxFg3FcH_smstrBOf_wSRDM",
            "pre_screening_backup_id": "1LREN6gUfMgllEd7g0IKWKQmZrAe2wMmIfivCG4o5teg",
            "screened_xlsx_snapshot_id": "1MnfmkDR8cuQGKz3nvT5i9O7rcyXyJdlS",
            "canonical_parent_id": "1zSfxpTs_hQyrp_D5b64IIfiszsGS3O2a",
            "canonical_shared": False,
            "canonical_permission": "owner only",
            "disposable_test_copy_deleted": True,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"external_files": len(payload["external_files"]), "repository_files": len(payload["repository_files"])}, indent=2))


if __name__ == "__main__":
    main()
