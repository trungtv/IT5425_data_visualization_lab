#!/usr/bin/env python3
"""Validate all lab notebooks are valid nbformat v4. Run in CI."""

from __future__ import annotations

import sys
from pathlib import Path

import nbformat
from nbformat.validator import normalize


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    labs = root / "labs"
    errors: list[str] = []
    targets = sorted(labs.glob("**/*.ipynb"))
    for path in targets:
        try:
            nb = nbformat.read(path, as_version=4)
            _, nbd = normalize(nb)
            nbformat.validate(nbformat.from_dict(nbd))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{path.relative_to(root)}: {exc}")

    if errors:
        print("Notebook validation failed:", file=sys.stderr)
        for line in errors:
            print(line, file=sys.stderr)
        return 1
    print(f"OK — {len(targets)} notebooks valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
