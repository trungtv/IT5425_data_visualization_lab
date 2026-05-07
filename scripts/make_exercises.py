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
        default=[],
        help=(
            "Relative lab paths under solutions/ (e.g. "
            "phase1_data_chart_basics/pandas_seaborn_eda). "
            "If omitted, auto-discover all solution.ipynb recursively."
        ),
    )
    args = parser.parse_args()

    labs = args.labs
    if not labs:
        labs = [
            str(path.parent.relative_to(ROOT / "solutions"))
            for path in sorted((ROOT / "solutions").glob("**/solution.ipynb"))
        ]

    for lab in labs:
        sol = ROOT / "solutions" / lab / "solution.ipynb"
        if not sol.exists():
            raise SystemExit(f"Missing solution notebook: {sol}")

        nb = nbformat.read(sol, as_version=4)
        ex = strip_and_hole(nb)

        out = ROOT / "labs" / lab / "lab.ipynb"
        out.parent.mkdir(parents=True, exist_ok=True)
        nbformat.write(ex, out)
        print("Wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main()

