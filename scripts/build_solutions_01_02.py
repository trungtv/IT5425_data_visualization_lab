#!/usr/bin/env python3
"""
Generate full-answer solution notebooks for Lab 01–02.

Run:
  .venv/bin/python scripts/build_solutions_01_02.py
"""

from __future__ import annotations

from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook


ROOT = Path(__file__).resolve().parents[1]


def md(text: str) -> nbformat.NotebookNode:
    return new_markdown_cell(text)


def code(text: str, *, tags: list[str] | None = None) -> nbformat.NotebookNode:
    c = new_code_cell(text)
    if tags:
        c.metadata["tags"] = tags
    return c


def write_nb(path: Path, nb: nbformat.NotebookNode) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(nb, path)


def build_lab01() -> nbformat.NotebookNode:
    cells: list[nbformat.NotebookNode] = [
        md(
            """# Lab 01 — Chương 1: Overview & Anscombe (Solution)

**Mục tiêu:** tái hiện Anscombe’s Quartet và nêu bài học về việc không chỉ dựa vào summary statistics.

**Đọc:** `related/english/chapter1.tex`
"""
        ),
        md("## Setup"),
        code(
            """import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
"""
        ),
        md("## Task 1 — Anscombe: summary stats vs scatter"),
        code(
            """df = sns.load_dataset("anscombe")
df.head()""",
            tags=["exercise"],
        ),
        code(
            """# Summary statistics per dataset
summary = (
    df.groupby("dataset")
    .agg(
        x_mean=("x", "mean"),
        y_mean=("y", "mean"),
        x_var=("x", "var"),
        y_var=("y", "var"),
        corr=("x", lambda s: s.corr(df.loc[s.index, "y"])),
    )
    .round(3)
)
summary""",
            tags=["exercise"],
        ),
        code(
            """# Scatter 2x2
fig, axes = plt.subplots(2, 2, figsize=(10, 8), sharex=True, sharey=True)
axes = axes.ravel()
for ax, (name, g) in zip(axes, df.groupby("dataset"), strict=True):
    ax.scatter(g["x"], g["y"])
    ax.set_title(f"Anscombe {name}")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
plt.tight_layout()
plt.show()""",
            tags=["exercise"],
        ),
        md(
            """## Task 2 — SciViz vs InfoViz (minh họa đơn giản)

Để minh họa *góc nhìn*:
- **Information viz**: cùng dữ liệu, tập trung “so sánh/quan hệ” → scatter.
- **Scientific-ish viz**: cùng dữ liệu, ép về “field”/“bề mặt” (minh họa) → ước lượng mật độ 2D.

Lưu ý: đây chỉ là minh họa ý niệm, không khẳng định Anscombe là SciViz.
"""
        ),
        code(
            """import numpy as np

g = df[df["dataset"] == "I"].copy()

# InfoViz: scatter (relationship)
plt.figure(figsize=(5, 4))
plt.scatter(g["x"], g["y"])
plt.title("InfoViz angle — relationship (scatter)")
plt.xlabel("x")
plt.ylabel("y")
plt.tight_layout()
plt.show()

# Scientific-ish angle: 2D density (field-like view)
plt.figure(figsize=(5, 4))
plt.hist2d(g["x"], g["y"], bins=(10, 10), cmap="viridis")
plt.colorbar(label="count")
plt.title("Scientific-ish angle — density field (hist2d)")
plt.xlabel("x")
plt.ylabel("y")
plt.tight_layout()
plt.show()""",
            tags=["exercise"],
        ),
        md(
            """## Reflection (mẫu)

- **Ba chức năng DV:** (1) ghi nhận, (2) phân tích/hình thành giả thuyết, (3) truyền thông.
  Trong bài này, Anscombe nhấn mạnh (2): dùng hình để *kiểm tra giả định* trước khi kết luận.
- **Bài học Anscombe:** 4 bộ có thống kê gần giống nhưng cấu trúc khác nhau → nếu chỉ nhìn mean/var/corr sẽ dễ kết luận sai.

**Họ tên / MSSV:** (điền khi chấm)
"""
        ),
    ]

    nb = new_notebook(
        cells=cells,
        metadata={
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
        },
    )
    return nbformat.validator.normalize(nb)[1]


def build_lab02() -> nbformat.NotebookNode:
    cells: list[nbformat.NotebookNode] = [
        md(
            """# Lab 02 — Chương 2: Visual models & encoding (Solution)

**Mục tiêu:** áp dụng Stevens (N/O/I/R) để chọn biểu đồ + encoding đúng.

**Đọc:** `related/english/chapter2.tex`
"""
        ),
        md("## Setup + load data (Gapminder)"),
        code(
            """from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

root = Path("..").resolve().parent  # từ solutions/lab02... về repo root
df = pd.read_csv(root / "data" / "gapminder.csv")
df.head()""",
            tags=["exercise"],
        ),
        md(
            """## Task — tạo một bảng (nominal, ordinal, ratio/interval, temporal)

Ta tạo bảng nhỏ từ Gapminder:
- **nominal**: `continent`
- **temporal**: `year`
- **ratio**: `gdpPercap`, `lifeExp` (xấp xỉ interval)
- **ordinal (tạo mới)**: nhóm `gdpPercap` theo quantile → `gdp_bin` (Low/Med/High)
"""
        ),
        code(
            """# Chuẩn bị bảng cho 1 năm để minh họa rõ
year = 2007
d = df[df["year"] == year].copy()

# Tạo ordinal bin (3 mức) từ ratio gdpPercap
d["gdp_bin"] = pd.qcut(d["gdpPercap"], q=3, labels=["Low", "Medium", "High"])

# Tổng hợp theo nominal + ordinal
agg = (
    d.groupby(["continent", "gdp_bin"], observed=True)
    .agg(mean_lifeExp=("lifeExp", "mean"), n=("country", "count"))
    .reset_index()
)
agg.head()""",
            tags=["exercise"],
        ),
        md(
            """## 1) Biểu đồ **sai encoding** (cố ý)

Ví dụ sai phổ biến: dùng **pie chart** để so sánh **mean_lifeExp** theo `continent`
(một đại lượng interval/ratio) — pie làm người xem so “góc/diện tích” kém chính xác,
và không phù hợp khi cần so sánh tương đối tinh.
"""
        ),
        code(
            """bad = agg.groupby("continent", as_index=False)["mean_lifeExp"].mean()

plt.figure(figsize=(6, 6))
plt.pie(bad["mean_lifeExp"], labels=bad["continent"], autopct="%.1f%%")
plt.title("BAD: Pie chart for mean life expectancy (hard to compare precisely)")
plt.show()""",
            tags=["exercise"],
        ),
        md(
            """## 2) Phiên bản **sửa** đúng nguyên tắc

Chọn **bar chart** (position/length) giúp so sánh chính xác hơn.
"""
        ),
        code(
            """good = bad.sort_values("mean_lifeExp", ascending=True)

plt.figure(figsize=(8, 4))
plt.barh(good["continent"], good["mean_lifeExp"])
plt.xlabel("Mean life expectancy")
plt.title("GOOD: Bar chart for mean life expectancy by continent (year=2007)")
plt.tight_layout()
plt.show()""",
            tags=["exercise"],
        ),
        md(
            """## Bonus: encoding cho temporal (time series)

Vì có `year` (temporal), line chart là phù hợp để xem trend.
"""
        ),
        code(
            """ts = (
    df.groupby(["year", "continent"], as_index=False)
    .agg(mean_lifeExp=("lifeExp", "mean"))
)

plt.figure(figsize=(9, 5))
for cont, g in ts.groupby("continent"):
    plt.plot(g["year"], g["mean_lifeExp"], label=cont)
plt.title("Mean life expectancy over time (line chart for temporal data)")
plt.xlabel("Year")
plt.ylabel("Mean life expectancy")
plt.legend(ncol=3, fontsize=9)
plt.tight_layout()
plt.show()""",
            tags=["exercise"],
        ),
        md(
            """## Reflection (mẫu)

- **Visual model:** temporal → line chart; comparison between categories → bar chart.
- **Marks & channels:** bar (length/position), line (position), color chỉ dùng để phân biệt nhóm (continent).
- **Vì sao pie sai:** so sánh diện tích/góc kém chính xác, không hỗ trợ so sánh fine-grained.

**Họ tên / MSSV:** (điền khi chấm)
"""
        ),
    ]

    nb = new_notebook(
        cells=cells,
        metadata={
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
        },
    )
    return nbformat.validator.normalize(nb)[1]


def main() -> None:
    write_nb(
        ROOT / "solutions" / "lab01_chapter1" / "solution.ipynb",
        build_lab01(),
    )
    write_nb(
        ROOT / "solutions" / "lab02_chapter2" / "solution.ipynb",
        build_lab02(),
    )
    print("Wrote solutions for Lab01–02")


if __name__ == "__main__":
    main()

