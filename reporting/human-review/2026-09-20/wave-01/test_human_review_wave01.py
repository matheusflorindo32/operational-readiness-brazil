import csv, json
from pathlib import Path
P=Path(__file__).resolve().parent
def rows(name):
    with (P/name).open(encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))
sel=rows("human-review-wave-01-selection.csv")
assert len(sel)==10 and len({r["evidence_id"] for r in sel})==10
hd=rows("human-decisions.csv")
assert len(hd)==10
for r in hd:
    assert r["Claim-Ready"]=="NO"
    for k,v in r.items():
        if k not in ("Evidence ID","Claim-Ready"):
            assert (v or "")==""
iv={r["evidence_id"]:r for r in rows("integrity-version-review.csv")}
for k in ("EV-1328","EV-0632","EV-0376"):
    assert iv[k]["vor_comparison"]=="VOR_COMPARISON_PENDING"
assert len(rows("pilot-05-preflight-selection.csv"))==10
rs=json.loads((P/"run-summary.json").read_text())
assert rs["human_reviews_completed"]==0 and rs["claim_ready_global"]==0
print("WAVE01_REGRESSION_PASS")
