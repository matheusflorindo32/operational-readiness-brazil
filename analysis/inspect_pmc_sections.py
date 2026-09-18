"""Render PMC JATS sections and tables as paragraph-indexed audit text."""

from __future__ import annotations

import argparse
import xml.etree.ElementTree as ET
from pathlib import Path


def clean(node: ET.Element | None) -> str:
    return " ".join("".join(node.itertext()).split()) if node is not None else ""


def render(path: Path) -> str:
    root = ET.parse(path).getroot()
    article = root.find(".//article") if root.tag != "article" else root
    if article is None:
        raise ValueError(f"No article in {path}")
    lines = [f"TITLE: {clean(article.find('.//article-meta/title-group/article-title'))}"]
    lines.append(f"ARTICLE_TYPE: {article.get('article-type', '')}")
    abstract = clean(article.find(".//article-meta/abstract"))
    if abstract:
        lines.append(f"ABSTRACT: {abstract}")
    body = article.find("./body")
    if body is not None:
        for section in body.iter("sec"):
            title = clean(section.find("./title")) or "UNTITLED"
            paragraphs = section.findall("./p")
            if not paragraphs:
                continue
            lines.append(f"\n## {title}")
            for index, paragraph in enumerate(paragraphs, 1):
                lines.append(f"P{index}: {clean(paragraph)}")
    for index, table in enumerate(article.findall(".//table-wrap"), 1):
        lines.append(f"\n## TABLE {index}: {clean(table.find('./label'))} {clean(table.find('./caption'))}")
        for row in table.findall(".//tr"):
            cells = [clean(cell) for cell in list(row) if cell.tag.rsplit("}", 1)[-1] in {"th", "td"}]
            if cells:
                lines.append(" | ".join(cells))
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    for source in args.paths:
        target = args.output / f"{source.stem}.txt"
        target.write_text(render(source), encoding="utf-8")
        print(f"{source.name}\t{target}\t{target.stat().st_size}")
