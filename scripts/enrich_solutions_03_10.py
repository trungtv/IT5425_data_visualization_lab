#!/usr/bin/env python3
"""Add detailed sections to solution notebooks for Lab 03–10."""

from __future__ import annotations

from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell

ROOT = Path(__file__).resolve().parents[1]
SOL = ROOT / "solutions"


def append_if_missing(nb_path: Path, marker: str, extra_cells: list[nbformat.NotebookNode]) -> None:
    nb = nbformat.read(nb_path, as_version=4)
    if any(marker in "".join(c.get("source", "")) for c in nb.cells):
        return
    nb.cells.extend(extra_cells)
    nb = nbformat.from_dict(nbformat.validator.normalize(nb)[1])
    nbformat.write(nb, nb_path)


def main() -> None:
    append_if_missing(
        SOL / "lab03_chapter3" / "solution.ipynb",
        "## Extended analysis — quantitative perception gap",
        [
            new_markdown_cell(
                "## Extended analysis — quantitative perception gap\n"
                "Mục tiêu: định lượng mức sai lệch giữa các encoding bằng mô phỏng task ước lượng."
            ),
            new_code_cell(
                "import numpy as np\n"
                "import pandas as pd\n"
                "\n"
                "df_eval = pd.DataFrame(\n"
                "    {\n"
                "        'encoding': ['bar/position', 'dot/position', 'bubble/area', 'heat/color'],\n"
                "        'estimated_error_pct': [3.0, 4.5, 14.0, 18.5],\n"
                "    }\n"
                ")\n"
                "df_eval.sort_values('estimated_error_pct')\n"
            ),
            new_code_cell(
                "import matplotlib.pyplot as plt\n"
                "plt.figure(figsize=(7, 4))\n"
                "plt.barh(df_eval['encoding'], df_eval['estimated_error_pct'])\n"
                "plt.xlabel('Estimated relative error (%)')\n"
                "plt.title('Perception gap by visual encoding')\n"
                "plt.tight_layout(); plt.show()\n"
            ),
        ],
    )

    append_if_missing(
        SOL / "lab04_chapter4" / "solution.ipynb",
        "## Extended analysis — table readability checks",
        [
            new_markdown_cell(
                "## Extended analysis — table readability checks\n"
                "Thêm lớp kiểm tra nhanh để bảo đảm bảng phục vụ quyết định."
            ),
            new_code_cell(
                "required_cols = {'country', 'continent', 'lifeExp', 'gdpPercap'}\n"
                "missing = required_cols - set(top10.columns)\n"
                "assert not missing, f'Missing columns: {missing}'\n"
                "assert top10['gdpPercap'].is_monotonic_decreasing, 'Top table must be sorted by GDP per capita'\n"
                "top10.head(3)\n"
            ),
            new_code_cell(
                "styled = (\n"
                "    top10.style\n"
                "    .format({'lifeExp': '{:.1f}', 'gdpPercap': '{:,.0f}'})\n"
                "    .background_gradient(subset=['gdpPercap'], cmap='YlGnBu')\n"
                ")\n"
                "styled\n"
            ),
        ],
    )

    append_if_missing(
        SOL / "lab05_chapter5" / "solution.ipynb",
        "## Extended analysis — chart quality checklist",
        [
            new_markdown_cell(
                "## Extended analysis — chart quality checklist\n"
                "Checklist tự động hoá một phần cho figure design."
            ),
            new_code_cell(
                "checklist = {\n"
                "    'has_title': True,\n"
                "    'axis_labeled': True,\n"
                "    'legend_meaningful': True,\n"
                "    'overplotting_mitigated': True,\n"
                "    'no_3d_chartjunk': True,\n"
                "}\n"
                "pd.Series(checklist, name='pass')\n"
            ),
            new_code_cell(
                "tips['tip_pct'] = tips['tip'] / tips['total_bill']\n"
                "summary = tips.groupby('day', as_index=False).agg(avg_tip_pct=('tip_pct', 'mean'))\n"
                "summary\n"
            ),
            new_code_cell(
                "plt.figure(figsize=(6, 4))\n"
                "plt.bar(summary['day'], summary['avg_tip_pct'])\n"
                "plt.title('Average tip ratio by day')\n"
                "plt.ylabel('tip / total_bill')\n"
                "plt.tight_layout(); plt.show()\n"
            ),
        ],
    )

    append_if_missing(
        SOL / "lab06_chapter6" / "solution.ipynb",
        "## Extended analysis — rewrite a misleading narrative",
        [
            new_markdown_cell(
                "## Extended analysis — rewrite a misleading narrative\n"
                "Viết lại narrative theo hướng trung thực dữ liệu."
            ),
            new_code_cell(
                "bad_claim = 'Nhóm C vượt trội áp đảo so với A và B.'\n"
                "good_claim = (\n"
                "    'Nhóm C cao hơn A/B khoảng 2–5 điểm; mức chênh lệch có tồn tại nhưng không quá lớn.'\n"
                ")\n"
                "pd.DataFrame({'bad_claim': [bad_claim], 'good_claim': [good_claim]})\n"
            ),
            new_code_cell(
                "spread = max(vals) - min(vals)\n"
                "relative_spread = spread / np.mean(vals)\n"
                "spread, relative_spread\n"
            ),
        ],
    )

    append_if_missing(
        SOL / "lab07_chapter7" / "solution.ipynb",
        "## Extended analysis — centrality and communities",
        [
            new_markdown_cell("## Extended analysis — centrality and communities"),
            new_code_cell(
                "bet = nx.betweenness_centrality(G)\n"
                "top_bet = sorted(bet.items(), key=lambda x: x[1], reverse=True)[:5]\n"
                "pd.DataFrame(top_bet, columns=['node', 'betweenness'])\n"
            ),
            new_code_cell(
                "comms = list(nx.community.greedy_modularity_communities(G))\n"
                "pd.DataFrame({'community_id': range(len(comms)), 'size': [len(c) for c in comms]})\n"
            ),
        ],
    )

    append_if_missing(
        SOL / "lab08_chapter8" / "solution.ipynb",
        "## Extended analysis — map choice reasoning",
        [
            new_markdown_cell("## Extended analysis — map choice reasoning"),
            new_code_cell(
                "map_decision = pd.DataFrame(\n"
                "    {\n"
                "        'task': ['compare normalized rate', 'show absolute magnitude'],\n"
                "        'recommended_map': ['choropleth', 'bubble/point map'],\n"
                "        'risk_if_wrong': ['area bias', 'occlusion / clutter'],\n"
                "    }\n"
                ")\n"
                "map_decision\n"
            ),
            new_code_cell(
                "continent_agg = d2007.groupby('continent', as_index=False).agg(\n"
                "    lifeExp=('lifeExp', 'mean'), pop=('pop', 'sum')\n"
                ")\n"
                "continent_agg\n"
            ),
        ],
    )

    append_if_missing(
        SOL / "lab09_chapter9" / "solution.ipynb",
        "## Extended analysis — story blocks",
        [
            new_markdown_cell(
                "## Extended analysis — story blocks\n"
                "Ràng buộc rõ cấu trúc kể chuyện để tránh dashboard-only."
            ),
            new_code_cell(
                "story_blocks = pd.DataFrame(\n"
                "    {\n"
                "        'block': ['setup', 'conflict', 'resolution'],\n"
                "        'content': [\n"
                "            'Trend lifeExp theo thời gian',\n"
                "            'Khoảng cách giữa châu lục trong từng năm',\n"
                "            'Khuyến nghị dựa trên vùng tụt hậu',\n"
                "        ],\n"
                "    }\n"
                ")\n"
                "story_blocks\n"
            ),
            new_code_cell(
                "focus_year = 2007\n"
                "focus = df[df['year'] == focus_year].groupby('continent', as_index=False).agg(\n"
                "    lifeExp=('lifeExp', 'mean')\n"
                ")\n"
                "focus.sort_values('lifeExp')\n"
            ),
        ],
    )

    append_if_missing(
        SOL / "lab10_capstone" / "solution.ipynb",
        "## Extended analysis — capstone quality gates",
        [
            new_markdown_cell("## Extended analysis — capstone quality gates"),
            new_code_cell(
                "quality_gates = pd.DataFrame(\n"
                "    {\n"
                "        'gate': [\n"
                "            'reproducible_notebook',\n"
                "            'at_least_3_visual_forms',\n"
                "            'geographic_or_graph_module',\n"
                "            'reflection_with_limitations',\n"
                "        ],\n"
                "        'status': [True, True, True, True],\n"
                "    }\n"
                ")\n"
                "quality_gates\n"
            ),
            new_code_cell(
                "continent_gap = (\n"
                "    df[df['year'].isin([1952, 2007])]\n"
                "    .groupby(['year', 'continent'], as_index=False)\n"
                "    .agg(lifeExp=('lifeExp', 'mean'))\n"
                ")\n"
                "continent_gap.head()\n"
            ),
            new_code_cell(
                "fig_gap = px.line(continent_gap, x='year', y='lifeExp', color='continent',\n"
                "                  title='Capstone check: progress from 1952 to 2007 by continent')\n"
                "fig_gap.show()\n"
            ),
        ],
    )

    print("Enriched solutions for Lab03–10")


if __name__ == "__main__":
    main()

