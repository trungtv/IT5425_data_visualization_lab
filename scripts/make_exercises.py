#!/usr/bin/env python3
"""
Generate exercise notebooks in `labs/` from `solutions/`.

Rules:
- Strip outputs + execution_count.
- For code cells tagged `exercise`, replace source with a short TODO stub.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]


def to_todo_stub(src: str) -> str:
    # Keep imports if present; blank the rest to force student work.
    lines = src.splitlines()
    kept: list[str] = []
    for line in lines:
        if line.startswith("import ") or line.startswith("from "):
            kept.append(line)
    kept.append("")
    kept.append("# TODO: hoàn thiện cell này theo đề bài")
    kept.append("")
    return "\n".join(kept) + "\n"


def strip_and_hole(nb: nbformat.NotebookNode) -> nbformat.NotebookNode:
    nb2 = nbformat.from_dict(nbformat.validator.normalize(nb)[1])
    for cell in nb2.cells:
        if cell.get("cell_type") == "code":
            cell["execution_count"] = None
            cell["outputs"] = []
            tags = cell.get("metadata", {}).get("tags", [])
            if "exercise" in tags:
                cell["source"] = to_todo_stub(cell.get("source", ""))
    return nb2


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--labs",
        nargs="*",
        default=[
            "lab01_chapter1",
            "lab02_chapter2",
            "lab03_chapter3",
            "lab04_chapter4",
            "lab05_chapter5",
            "lab06_chapter6",
            "lab07_chapter7",
            "lab08_chapter8",
            "lab09_chapter9",
            "lab10_capstone",
        ],
    )
    args = parser.parse_args()

    for lab in args.labs:
        sol = ROOT / "solutions" / lab / "solution.ipynb"
        if not sol.exists():
            raise SystemExit(f"Missing solution notebook: {sol}")

        nb = nbformat.read(sol, as_version=4)
        ex = strip_and_hole(nb)

        # output name convention: lab01.ipynb, lab02.ipynb
        num = lab.split("_", 1)[0].replace("lab", "")
        out = ROOT / "labs" / lab / f"lab{num}.ipynb"
        out.parent.mkdir(parents=True, exist_ok=True)
        nbformat.write(ex, out)
        print("Wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main()

