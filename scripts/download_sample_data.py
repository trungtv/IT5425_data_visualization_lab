#!/usr/bin/env python3
"""
Tải và lưu Gapminder (Plotly) ra data/gapminder.csv — dùng xuyên các lab (map, scatter, time).
Chạy: python scripts/download_sample_data.py
"""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data" / "gapminder.csv",
        help="Output CSV path",
    )
    args = parser.parse_args()
    args.out.parent.mkdir(parents=True, exist_ok=True)

    import plotly.express as px

    df = px.data.gapminder()
    df.to_csv(args.out, index=False)
    print(f"Wrote {args.out} ({len(df)} rows, {len(df.columns)} columns)")


if __name__ == "__main__":
    main()
