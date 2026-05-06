#!/usr/bin/env python3
"""One-off generator for lab notebooks (valid nbformat 4). Run: python scripts/build_labs.py"""
from __future__ import annotations

from pathlib import Path

import nbformat
from nbformat.validator import normalize

ROOT = Path(__file__).resolve().parents[1]
LABS = ROOT / "labs"

META = {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python", "version": "3.11.0"},
}


def nb(cells: list) -> dict:
    return {"nbformat": 4, "nbformat_minor": 5, "metadata": META, "cells": cells}


def md(text: str) -> dict:
    lines = [line if line.endswith("\n") else line + "\n" for line in text.split("\n")]
    if lines and not lines[-1].endswith("\n"):
        lines[-1] += "\n"
    return {"cell_type": "markdown", "metadata": {}, "source": lines}


def code(text: str) -> dict:
    lines = [line if line.endswith("\n") else line + "\n" for line in text.split("\n")]
    if lines and not lines[-1].endswith("\n"):
        lines[-1] += "\n"
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": lines,
    }


LABS_SPEC: list[tuple[str, str, list]] = [
    (
        "lab01_chapter1",
        "lab01.ipynb",
        [
            md(
                """# Lab 01 — Chương 1: Overview & Anscombe

**Mục tiêu:** Nhắc lại vai trò của visualization; tái hiện Anscombe’s Quartet; phân biệt góc nhìn *Scientific vs Information* visualization.

**Đọc:** `related/english/chapter1.tex` (Anscombe, Types of DV)."""
            ),
            md("## Task 1 — Anscombe\nTải dataset Anscombe (có sẵn trong Seaborn), in summary statistics cho từng nhóm, vẽ scatter. So sánh kết luận."),
            code(
                """import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# TODO: load sns.load_dataset("anscombe")
# TODO: groupby("dataset") và mô tả thống kê
# TODO: FacetGrid hoặn subplots 2x2 scatter
"""
            ),
            md(
                """## Task 2 — SciViz vs InfoViz
Với **một** dataset bạn chọn (Anscombe hoặc dataset khác), tạo **hai** hình:
1. Nhấn mạnh **mô phỏng / không gian / vật lý hóa trừu tượng** (giả lập Scientific angle — có thể đơn giản hóa).
2. Nhấn mạnh **tóm tắt trừu tượng / hỗ trợ quyết định** (Information angle).

Viết 1 đoạn so sánh đặc điểm hai loại theo sách."""
            ),
            code("# TODO: Hai visualization + export fig\n"),
            md(
                """## Reflection (bắt buộc)

- Ba chức năng của DV (ghi nhận / phân tích / truyền thông) — áp vào bài làm.
- Anscombe dạy điều gì về *chỉ nhìn summary statistics*?

**Họ tên / MSSV:**"""
            ),
        ],
    ),
    (
        "lab02_chapter2",
        "lab02.ipynb",
        [
            md(
                """# Lab 02 — Chương 2: Visual models & encoding

**Mục tiêu:** Áp dụng phân loại thuộc tính Stevens (N,O,I,R); chọn visual model + channel hợp lý.

**Đọc:** `related/english/chapter2.tex` (Data attributes, Visual encoding)."""
            ),
            md(
                """## Task — Cùng một data table
Dùng một bảng có ít nhất: 1 nominal, 1 ordinal, 1 ratio/interval, 1 temporal (có thể tạo synthetic).

1. Vẽ **một biểu đồ sai encoding** (cố ý) và giải thích vì sao sai.
2. Vẽ **phiên bản sửa** đúng nguyên tắc."""
            ),
            code(
                """import pandas as pd
import matplotlib.pyplot as plt

# TODO: tạo hoặc đọc df
# TODO: bad chart + good chart
"""
            ),
            md(
                """## Reflection

- Visual model bạn chọn (linear / temporal / 2D scatter / …) map thế nào vào data?
- Marks & channels đã dùng? Có redundant encoding không (xem trước Ch.5 nếu muốn)?

**Họ tên / MSSV:**"""
            ),
        ],
    ),
    (
        "lab03_chapter3",
        "lab03.ipynb",
        [
            md(
                """# Lab 03 — Chương 3: Graphical perception

**Mục tiêu:** So sánh độ dễ đọc giữa các channel (ví dụ position vs area vs color intensity) trên **cùng một tác vụ ước lượng**.

**Đọc:** `related/english/chapter3.tex`"""
            ),
            md(
                """## Task
Tạo **3–4** phiên bản cùng một thông điệp so sánh (ví dụ: 4–5 giá trị) dùng:
- bar h (position+length)
- dot / lollipop
- bubble (area)
- choropleth-like fake hoặc heat strip (color saturation)

Ghi **subjective rank** + **lỗi ước lượng %** nếu bạn tự khảo sát được bạn bè (optional). Ít nhất: phân tích định tính trong reflection."""
            ),
            code(
                """import matplotlib.pyplot as plt
import numpy as np

values = np.array([12, 19, 8, 25, 15])
labels = list("ABCDE")
# TODO: 3–4 charts
"""
            ),
            md(
                """## Reflection

Kết nối với các *elements of graphical perception* và *order of accuracy* (trích từ giáo trình / Cleveland).

**Họ tên / MSSV:**"""
            ),
        ],
    ),
    (
        "lab04_chapter4",
        "lab04.ipynb",
        [
            md(
                """# Lab 04 — Chương 4: Table visualization

**Mục tiêu:** Thiết kế bảng cho **đọc nhanh** và **xuất báo cáo**; dùng heat-style cho ma trận số.

**Đọc:** `related/english/chapter4.tex`"""
            ),
            md(
                """## Task
1. Một **table** exploratory (pandas Styler hoặc heatmap của correlation matrix).
2. Một **table** kiểu publication: rõ nhóm hàng/cột, alignment số — có thể dùng matplotlib.table hoặc export HTML từ Styler.

So sánh khi nào dùng loại nào."""
            ),
            code(
                """import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# TODO: corr heatmap + styled table hoặc matplotlib.table
"""
            ),
            md(
                """## Reflection

Viết ngắn về *key/value structure* và alignment theo đúng từ vựng chương 4.

**Họ tên / MSSV:**"""
            ),
        ],
    ),
    (
        "lab05_chapter5",
        "lab05.ipynb",
        [
            md(
                """# Lab 05 — Chương 5: Principles of figure design

**Mục tiêu:** Before/After: overlapping points → jitter/violin/sample; palette có ý đồ; small multiples.

**Đọc:** `related/english/chapter5.tex`"""
            ),
            md(
                """## Task

1. Lấy (hoặc tạo) scatter có **nhiều chồng lấn** — biểu diễn trước/sau (alpha, jitter, hexbin, 2D density — chọn 1–2).

2. Một nhóm **small multiples** (facet) cho biến phân nhóm.

3. Tránh pseudo-3D / pie không cần thiết: nếu đã có trong data story, chỉnh lại."""
            ),
            code(
                """import seaborn as sns
import matplotlib.pyplot as plt

# TODO: seaborn không có tips thì sns.load_dataset
"""
            ),
            md(
                """## Reflection

Nêu rõ đã áp dụng: data-ink, color role, captions — theo các mục đã học trong Ch.5.

**Họ tên / MSSV:**"""
            ),
        ],
    ),
    (
        "lab06_chapter6",
        "lab06.ipynb",
        [
            md(
                """# Lab 06 — Chương 6: The Good, The Bad, and The Weird

**Mục tiêu:** Phê bình visualization; redesign theo checklist.

**Đọc:** `related/english/chapter6.tex`"""
            ),
            md(
                """## Task
1. Mang **ít nhất 2** ví dụ Bad (báo chí / Twitter / chủ đích sai).
2. Liệt kê checklist vi phạm (trục, scale, cherry-picking, chartjunk…).
3. **Redesign** bằng Python (ưu tiên) hoặc mô phỏng sketch + code."""
            ),
            code(
                """# TODO: paste link nguồn + comment
import matplotlib.pyplot as plt
"""
            ),
            md(
                """## Reflection

Phân loại Good/Bad/Weird và lý luận trung thực dữ liệu.

**Họ tên / MSSV:**"""
            ),
        ],
    ),
    (
        "lab07_chapter7",
        "lab07.ipynb",
        [
            md(
                """# Lab 07 — Chương 7: Graph visualization

**Mục tiêu:** Visualize một graph nhỏ: layout + insight (subgraph hoặc path).

**Đọc:** `related/english/chapter7.tex`"""
            ),
            md(
                "Dùng `networkx` + `matplotlib` (hoặc `plotly`). Graph 10–40 nodes. Ghi chú *tại sao chọn layout này*."
            ),
            code(
                """import networkx as nx
import matplotlib.pyplot as plt

# TODO: G = nx.karate_club_graph() hoặc graph tự xây
"""
            ),
            md(
                """## Reflection

Giới hạn khi graph lớn (aggregation, sampling) — một đoạn.

**Họ tên / MSSV:**"""
            ),
        ],
    ),
    (
        "lab08_chapter8",
        "lab08.ipynb",
        [
            md(
                """# Lab 08 — Chương 8: Geographic visualization

**Mục tiêu:** So sánh **choropleth** vs **point/bubble** map; nêu cảnh báo về aggregation (MAUP) ở mức khái niệm.

**Đọc:** `related/english/chapter8.tex`"""
            ),
            md(
                """## Task
Dùng Plotly (`px.choropleth` + `scatter_geo` hoặc `scatter_mapbox`) với một dataset có cột quốc gia ISO-3 hoặc lat/lon.
- Ít nhất **hai** kiểu bản đồ cho cùng một biến (hoặc hai biến liên quan).
- Reflection: khi nào nên / không nên choropleth."""
            ),
            code(
                """import plotly.express as px

# TODO: px.data.gapminder() hoặc tự có df
"""
            ),
            md(
                """## Reflection

Kết nối với *guidelines for choosing visualization methods* trong chương 8.

**Họ tên / MSSV:**"""
            ),
        ],
    ),
    (
        "lab09_chapter9",
        "lab09.ipynb",
        [
            md(
                """# Lab 09 — Chương 9: Data storytelling + interaction

**Mục tiêu:** Gói phân tích thành **mini app Streamlit**: luồng narrative + ít nhất một điều khiển (select/slider).

**Đọc:** `related/english/chapter9.tex`"""
            ),
            md(
                "Hoàn thiện `app.py` trong thư mục này. Notebook dùng để prototype chart; báo cáo links/glue giữa section Streamlit và insight."
            ),
            code("# Prototype trong notebook — copy sang app.py\nimport plotly.express as px\n"),
            md(
                """## Reflection

Áp các *fundamental principles* storytelling trong chương 9 vào luồng app.

**Họ tên / MSSV:**

**Chạy app:** `streamlit run app.py` (từ thư mục lab09)."""
            ),
        ],
    ),
    (
        "lab10_capstone",
        "lab10.ipynb",
        [
            md(
                """# Lab 10 — Capstone

**Yêu cầu:**

1. **Notebook** đầy đủ EDA → insight (có citing figure design Ch.5–6).

2. **Sản phẩm**: Streamlit hoặc bộ slide export từ notebook — phải có **story arc** rõ.

3. Bắt buộc có **ít nhất một** trong: geographic (Ch.8) hoặc graph (Ch.7).

4. Có một mục **redesign/critique** (tự phê bình bản nháp → bản cuối).

Nộp cả notebook + link repo / screenshot app.

**Đọc lại:** toàn bộ minitoc các chương liên quan phần bạn viết báo cáo."""
            ),
            code("# Capstone workspace\n"),
            md("## Timeline checklist (điền)\n\n| Milestone | Ngày |\n|-----------|------|\n| Dataset locked | |\n| First draft viz | |\n| Critique peer/GV | |\n| Final | |\n\n**Họ tên / MSSV:**"),
        ],
    ),
]


def main() -> None:
    for folder, fname, cells in LABS_SPEC:
        path = LABS / folder / fname
        path.parent.mkdir(parents=True, exist_ok=True)
        _, nbd = normalize(nb(cells))
        nbformat.write(nbformat.from_dict(nbd), path)
        print("Wrote", path)


if __name__ == "__main__":
    main()
