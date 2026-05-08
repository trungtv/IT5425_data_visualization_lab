#!/usr/bin/env python3
"""
Download and preprocess an OWID CO2 panel subset for labs.

Run:
  python scripts/download_owid_co2_subset.py
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

OWID_CO2_URL = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data" / "owid_co2_subset.csv",
        help="Output CSV path",
    )
    parser.add_argument(
        "--min-year",
        type=int,
        default=1990,
        help="Minimum year to keep (inclusive).",
    )
    args = parser.parse_args()
    args.out.parent.mkdir(parents=True, exist_ok=True)

    cols = [
        "country",
        "iso_code",
        "year",
        "population",
        "gdp",
        "co2",
        "co2_per_capita",
        "methane",
        "nitrous_oxide",
        "energy_per_capita",
        "primary_energy_consumption",
        "coal_co2",
        "oil_co2",
        "gas_co2",
        "temperature_change_from_ghg",
        "trade_co2",
    ]

    df = pd.read_csv(OWID_CO2_URL, usecols=cols)
    df = df[df["year"] >= args.min_year].copy()
    df = df[df["iso_code"].str.len() == 3].copy()
    df = df.sort_values(["country", "year"]).reset_index(drop=True)
    df.to_csv(args.out, index=False)
    print(f"Wrote {args.out} ({len(df)} rows, {len(df.columns)} columns)")


if __name__ == "__main__":
    main()
