"""Preserve pre-analysis workbook, stable identities and a verified local DB snapshot."""

import csv
import hashlib
import json
import shutil
import sqlite3
from pathlib import Path

from audit_pubmed_structure import ROOT, WORKBOOK, workbook_cells


def main():
    backup = ROOT.parents[1] / "outputs/zotero-backups/2026-09-06-preanalysis"
    if (ROOT / "reporting/preanalysis/2026-09-06/backup-manifest.json").exists():
        raise FileExistsError(
            "Pre-analysis backup already recorded; never overwrite it."
        )
    backup.mkdir(parents=True, exist_ok=True)
    report_dir = ROOT / "reporting/preanalysis/2026-09-06"
    report_dir.mkdir(parents=True, exist_ok=True)
    target = backup / WORKBOOK.name
    shutil.copy2(WORKBOOK, target)
    assert WORKBOOK.read_bytes() == target.read_bytes()
    cells = workbook_cells(WORKBOOK)["Master Evidence"]
    rows = [
        {
            "evidence_id": cells[f"A{r}"],
            "pmid": cells[f"X{r}"],
            "zotero_key": cells[f"AF{r}"],
        }
        for r in range(4, 1460)
    ]
    for key in rows[0]:
        assert len({x[key] for x in rows}) == 1456 and all(x[key] for x in rows)
    assert next(x for x in rows if x["pmid"] == "26159007") == {
        "evidence_id": "EV-1171",
        "pmid": "26159007",
        "zotero_key": "9UE7LEZP",
    }
    mapping = report_dir / "evidence-identity-map.csv"
    with mapping.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    shutil.copy2(mapping, backup / mapping.name)
    old_manifest = json.loads(
        (
            ROOT / "reporting/zotero-runs/2026-09-02T13-40-38-0300/backup-manifest.json"
        ).read_text(encoding="utf-8-sig")
    )
    source = Path(old_manifest["source_database"])
    db_target = backup / "zotero-consistent-snapshot.sqlite"
    # Zotero can hold an exclusive lock: copy only while every source byte is
    # unchanged across the copy window. Recover WAL solely in the backup copy.
    sources = [p for p in (source, Path(str(source) + "-wal")) if p.exists()]
    before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    for p in sources:
        dest = db_target if p == source else Path(str(db_target) + "-wal")
        shutil.copy2(p, dest)
        assert hashlib.sha256(dest.read_bytes()).hexdigest() == before[p]
    assert before == {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    assert sources == [p for p in (source, Path(str(source) + "-wal")) if p.exists()]
    with sqlite3.connect(db_target) as db:
        integrity = db.execute("PRAGMA integrity_check").fetchone()[0]
        count = db.execute(
            "SELECT COUNT(*) FROM items WHERE itemID NOT IN (SELECT itemID FROM itemNotes) AND itemID NOT IN (SELECT itemID FROM itemAttachments) AND itemID NOT IN (SELECT itemID FROM deletedItems)"
        ).fetchone()[0]
        keys = {r[0] for r in db.execute("SELECT key FROM items")}
    assert integrity == "ok" and count == 1457
    assert {r["zotero_key"] for r in rows} <= keys
    db.close()
    files = [
        {
            "file": p.name,
            "bytes": p.stat().st_size,
            "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
            "valid_backup": p.stat().st_size > 0
            and not p.name.endswith(("-wal", "-shm")),
        }
        for p in backup.iterdir()
        if p.is_file()
    ]
    manifest = {
        "backup_location": "External project outputs/zotero-backups/2026-09-06-preanalysis",
        "files": files,
        "sqlite_integrity": integrity,
        "top_level_items": count,
        "identity_rows": len(rows),
        "source_read_only": True,
        "zotero_writes": 0,
        "method": "Database/WAL bytes stable before, during and after copy; recovery and integrity check in backup only.",
        "initial_online_backup": "Interrupted while blocked; zero-byte zotero-preanalysis.sqlite is invalid and excluded from valid backup and Git.",
    }
    (report_dir / "backup-manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
