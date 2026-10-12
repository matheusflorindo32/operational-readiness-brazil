"""Structural regression tests for Batch 11.4R artifacts without runtime XLSX libraries."""
from pathlib import Path
import csv, hashlib, json, zipfile
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'batch11_4r'
EXPECTED = {
 'International_v1.4-JOH-MANUAL-REVIEW-EN.docx',
 'International_v1.4-JOH-MANUAL-REVIEW-PTBR.docx',
 'International_v1.4-JOH-PREMIUM-ELITE-MANUAL-REVIEW.xlsx',
 'BILINGUAL_TRANSLATION_AUDIT.csv','MANUAL_REVIEW_PACKAGE_VALIDATION.md',
 'BATCH11_4R_MANIFEST.json','BATCH11_4R_REPORT.md',
}

def test_required_package_artifacts_exist():
 assert EXPECTED <= {x.name for x in OUT.iterdir()}

def test_english_review_docx_is_binary_source_copy():
 source=ROOT/'batch11_4'/'International_v1.4-JOH-EDITORIAL-ADAPTED.docx'
 out=OUT/'International_v1.4-JOH-MANUAL-REVIEW-EN.docx'
 assert hashlib.sha256(source.read_bytes()).digest()==hashlib.sha256(out.read_bytes()).digest()

def test_docx_ooxml_parts_exist():
 for name in ['International_v1.4-JOH-MANUAL-REVIEW-EN.docx','International_v1.4-JOH-MANUAL-REVIEW-PTBR.docx']:
  with zipfile.ZipFile(OUT/name) as z:
   assert z.testzip() is None
   assert 'word/document.xml' in z.namelist()

def test_workbook_has_twenty_ordered_human_review_sheets():
 xlsx=OUT/'International_v1.4-JOH-PREMIUM-ELITE-MANUAL-REVIEW.xlsx'
 with zipfile.ZipFile(xlsx) as z:
  assert z.testzip() is None
  root=ET.fromstring(z.read('xl/workbook.xml'))
  ns={'x':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
  names=[s.attrib['name'] for s in root.findall('x:sheets/x:sheet',ns)]
  assert len(names)==20
  assert [s[:2] for s in names]==[f'{i:02d}' for i in range(20)]
  assert 'xl/worksheets/sheet16.xml' in z.namelist()

def test_audit_and_manifest_pass():
 with (OUT/'BILINGUAL_TRANSLATION_AUDIT.csv').open(encoding='utf-8') as h:
  assert all(row['Result']=='PASS' for row in csv.DictReader(h))
 m=json.loads((OUT/'BATCH11_4R_MANIFEST.json').read_text(encoding='utf-8'))
 assert m['gate']=='BILINGUAL_MANUAL_REVIEW_PACKAGE_PASS'
 assert m['references']=='28/28' and m['claims']=='20/20'
 assert m['translation_drift']==0 and m['scientific_drift']==0
