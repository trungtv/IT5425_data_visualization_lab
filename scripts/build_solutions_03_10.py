#!/usr/bin/env python3
"""Generate full-answer solution notebooks for Lab 03–10."""

from __future__ import annotations

from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

ROOT = Path(__file__).resolve().parents[1]


def md(text: str):
    return new_markdown_cell(text)


def code(text: str, tags: list[str] | None = None):
    c = new_code_cell(text)
    if tags:
        c.metadata["tags"] = tags
    return c


def write_nb(path: Path, cells: list):
    nb = new_notebook(
        cells=cells,
        metadata={
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
        },
    )
    nb = nbformat.from_dict(nbformat.validator.normalize(nb)[1])
    path.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(nb, path)


def lab03_cells():
    return [
        md("# Lab 03 — Graphical perception (Solution)"),
        code(
            "import numpy as np\n"
            "import matplotlib.pyplot as plt\n"
            "import pandas as pd\n",
        ),
        md("So sánh cùng một thông điệp bằng các channels khác nhau."),
        code(
            "labels = list('ABCDE')\n"
            "values = np.array([12, 19, 8, 25, 15])\n"
            "df = pd.DataFrame({'label': labels, 'value': values})\n"
            "df",
            tags=["exercise"],
        ),
        code(
            "fig, axes = plt.subplots(2, 2, figsize=(12, 8))\n"
            "ax = axes[0, 0]\n"
            "ax.bar(df['label'], df['value'])\n"
            "ax.set_title('Bar (length/position)')\n"
            "ax = axes[0, 1]\n"
            "ax.scatter(df['label'], df['value'], s=100)\n"
            "ax.set_title('Dot plot (position)')\n"
            "ax = axes[1, 0]\n"
            "ax.scatter(df['label'], [1]*len(df), s=df['value']*30, alpha=0.7)\n"
            "ax.set_title('Bubble (area)')\n"
            "ax.set_yticks([])\n"
            "ax = axes[1, 1]\n"
            "heat = np.array([df['value'].values])\n"
            "im = ax.imshow(heat, cmap='viridis', aspect='auto')\n"
            "ax.set_xticks(range(len(df)))\n"
            "ax.set_xticklabels(df['label'])\n"
            "ax.set_yticks([])\n"
            "ax.set_title('Heat strip (color saturation)')\n"
            "fig.colorbar(im, ax=ax)\n"
            "plt.tight_layout()\n"
            "plt.show()",
            tags=["exercise"],
        ),
        md(
            "## Reflection\n"
            "- Position/length giúp ước lượng chính xác hơn area/color.\n"
            "- Bubble và color phù hợp overview, không tốt cho so sánh fine-grained.\n"
        ),
    ]


def lab04_cells():
    return [
        md("# Lab 04 — Table visualization (Solution)"),
        code(
            "from pathlib import Path\n"
            "import pandas as pd\n"
            "import seaborn as sns\n"
            "import matplotlib.pyplot as plt\n",
        ),
        code(
            "root = Path('..').resolve().parent\n"
            "df = pd.read_csv(root / 'data' / 'gapminder.csv')\n"
            "d2007 = df[df['year'] == 2007].copy()\n"
            "d2007.head()",
            tags=["exercise"],
        ),
        md("Exploratory table: correlation heatmap"),
        code(
            "num_cols = ['lifeExp', 'pop', 'gdpPercap']\n"
            "corr = d2007[num_cols].corr()\n"
            "plt.figure(figsize=(5, 4))\n"
            "sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')\n"
            "plt.title('Correlation matrix (2007)')\n"
            "plt.tight_layout()\n"
            "plt.show()",
            tags=["exercise"],
        ),
        md("Publication-style table: top 10 GDP per capita"),
        code(
            "top10 = d2007[['country', 'continent', 'lifeExp', 'gdpPercap']].sort_values(\n"
            "    'gdpPercap', ascending=False\n"
            ").head(10)\n"
            "top10.reset_index(drop=True)",
            tags=["exercise"],
        ),
        md(
            "## Reflection\n"
            "- Key/value và alignment số giúp đọc bảng nhanh.\n"
            "- Heat-style hữu ích khi cần nhận pattern hơn là đọc từng con số.\n"
        ),
    ]


def lab05_cells():
    return [
        md("# Lab 05 — Figure design principles (Solution)"),
        code(
            "import seaborn as sns\n"
            "import matplotlib.pyplot as plt\n"
            "import pandas as pd\n",
        ),
        code("tips = sns.load_dataset('tips')\n" "tips.head()", tags=["exercise"]),
        md("Before/after cho overlapping points"),
        code(
            "fig, axes = plt.subplots(1, 2, figsize=(12, 4), sharex=True, sharey=True)\n"
            "axes[0].scatter(tips['total_bill'], tips['tip'])\n"
            "axes[0].set_title('Before: raw scatter')\n"
            "sns.scatterplot(\n"
            "    data=tips,\n"
            "    x='total_bill',\n"
            "    y='tip',\n"
            "    hue='time',\n"
            "    alpha=0.7,\n"
            "    ax=axes[1],\n"
            ")\n"
            "axes[1].set_title('After: color + alpha')\n"
            "plt.tight_layout()\n"
            "plt.show()",
            tags=["exercise"],
        ),
        md("Small multiples"),
        code(
            "g = sns.FacetGrid(tips, col='sex', row='smoker', height=3)\n"
            "g.map_dataframe(sns.scatterplot, x='total_bill', y='tip', alpha=0.7)\n"
            "g.fig.suptitle('Small multiples by sex/smoker', y=1.02)\n"
            "plt.show()",
            tags=["exercise"],
        ),
        md(
            "## Reflection\n"
            "- Data-ink ratio tốt hơn khi loại bỏ yếu tố trang trí không cần thiết.\n"
            "- Small multiples giúp so sánh nhóm rõ hơn overlay quá nhiều màu.\n"
        ),
    ]


def lab06_cells():
    return [
        md("# Lab 06 — Good, Bad, Weird (Solution)"),
        code("import matplotlib.pyplot as plt\n" "import numpy as np\n"),
        md("Ví dụ bad chart tự tạo: cắt trục gây phóng đại khác biệt."),
        code(
            "cats = ['A', 'B', 'C']\n"
            "vals = [95, 98, 100]\n"
            "fig, axes = plt.subplots(1, 2, figsize=(10, 4))\n"
            "axes[0].bar(cats, vals)\n"
            "axes[0].set_ylim(90, 101)\n"
            "axes[0].set_title('BAD: truncated y-axis')\n"
            "axes[1].bar(cats, vals)\n"
            "axes[1].set_ylim(0, 110)\n"
            "axes[1].set_title('GOOD: full baseline')\n"
            "plt.tight_layout()\n"
            "plt.show()",
            tags=["exercise"],
        ),
        md(
            "## Reflection\n"
            "- Chart bad vì scale làm phóng đại chênh lệch nhỏ.\n"
            "- Bản sửa giữ baseline 0 nên diễn giải trung thực hơn.\n"
            "- Checklist: trục, scale, chú thích, nguồn dữ liệu.\n"
        ),
    ]


def lab07_cells():
    return [
        md("# Lab 07 — Graph visualization (Solution)"),
        code("import networkx as nx\n" "import matplotlib.pyplot as plt\n"),
        code(
            "G = nx.karate_club_graph()\n"
            "len(G), G.number_of_edges()",
            tags=["exercise"],
        ),
        code(
            "plt.figure(figsize=(8, 6))\n"
            "pos = nx.spring_layout(G, seed=42)\n"
            "nx.draw_networkx(\n"
            "    G,\n"
            "    pos=pos,\n"
            "    node_size=120,\n"
            "    with_labels=False,\n"
            "    edge_color='gray',\n"
            ")\n"
            "plt.title('Karate club graph — spring layout')\n"
            "plt.axis('off')\n"
            "plt.show()",
            tags=["exercise"],
        ),
        code(
            "deg = sorted(G.degree, key=lambda x: x[1], reverse=True)[:5]\n"
            "deg",
            tags=["exercise"],
        ),
        md(
            "## Reflection\n"
            "- Spring layout tốt cho graph nhỏ, trực quan về community.\n"
            "- Graph lớn cần sampling/aggregation để giảm rối.\n"
        ),
    ]


def lab08_cells():
    return [
        md("# Lab 08 — Geographic visualization (Solution)"),
        code(
            "from pathlib import Path\n"
            "import pandas as pd\n"
            "import plotly.express as px\n",
        ),
        code(
            "root = Path('..').resolve().parent\n"
            "df = pd.read_csv(root / 'data' / 'gapminder.csv')\n"
            "d2007 = df[df['year'] == 2007].copy()\n"
            "d2007.head()",
            tags=["exercise"],
        ),
        code(
            "fig1 = px.choropleth(\n"
            "    d2007,\n"
            "    locations='iso_alpha',\n"
            "    color='lifeExp',\n"
            "    hover_name='country',\n"
            "    color_continuous_scale='Viridis',\n"
            "    title='Life expectancy (choropleth, 2007)',\n"
            ")\n"
            "fig1.show()",
            tags=["exercise"],
        ),
        code(
            "fig2 = px.scatter_geo(\n"
            "    d2007,\n"
            "    locations='iso_alpha',\n"
            "    size='pop',\n"
            "    color='continent',\n"
            "    hover_name='country',\n"
            "    projection='natural earth',\n"
            "    title='Population bubbles (scatter_geo, 2007)',\n"
            ")\n"
            "fig2.show()",
            tags=["exercise"],
        ),
        md(
            "## Reflection\n"
            "- Choropleth tốt cho giá trị normalized theo vùng.\n"
            "- Bubble map tốt khi muốn nhấn mạnh magnitude theo điểm.\n"
        ),
    ]


def lab09_cells():
    return [
        md("# Lab 09 — Data storytelling (Solution)"),
        code(
            "from pathlib import Path\n"
            "import pandas as pd\n"
            "import plotly.express as px\n",
        ),
        code(
            "root = Path('..').resolve().parent\n"
            "df = pd.read_csv(root / 'data' / 'gapminder.csv')\n"
            "df.head()",
            tags=["exercise"],
        ),
        code(
            "trend = (\n"
            "    df.groupby(['year', 'continent'], as_index=False)\n"
            "    .agg(lifeExp=('lifeExp', 'mean'), gdpPercap=('gdpPercap', 'mean'))\n"
            ")\n"
            "fig = px.line(\n"
            "    trend,\n"
            "    x='year',\n"
            "    y='lifeExp',\n"
            "    color='continent',\n"
            "    title='Story step 1: life expectancy trend by continent',\n"
            ")\n"
            "fig.show()",
            tags=["exercise"],
        ),
        md(
            "Notebook này là prototype; sản phẩm chính nằm ở "
            "`solutions/lab09_chapter9/app.py`."
        ),
        md(
            "## Reflection\n"
            "- Story arc: mở đầu bằng trend dài hạn, sau đó drill-down theo năm.\n"
            "- Interaction trong app giúp người đọc tự kiểm chứng insight.\n"
        ),
    ]


def lab10_cells():
    return [
        md("# Lab 10 — Capstone (Solution skeleton with real outputs)"),
        code(
            "from pathlib import Path\n"
            "import pandas as pd\n"
            "import plotly.express as px\n"
            "import networkx as nx\n"
            "import matplotlib.pyplot as plt\n",
        ),
        code(
            "root = Path('..').resolve().parent\n"
            "df = pd.read_csv(root / 'data' / 'gapminder.csv')\n"
            "df.shape",
            tags=["exercise"],
        ),
        md("EDA + insight #1 (time trend)"),
        code(
            "trend = df.groupby('year', as_index=False).agg(lifeExp=('lifeExp', 'mean'))\n"
            "fig = px.line(trend, x='year', y='lifeExp', title='Global mean life expectancy')\n"
            "fig.show()",
            tags=["exercise"],
        ),
        md("Geographic component (Ch.8)"),
        code(
            "d2007 = df[df['year'] == 2007]\n"
            "fig2 = px.choropleth(d2007, locations='iso_alpha', color='lifeExp', title='LifeExp map 2007')\n"
            "fig2.show()",
            tags=["exercise"],
        ),
        md("Graph component nhẹ (Ch.7)"),
        code(
            "continents = sorted(df['continent'].unique())\n"
            "G = nx.Graph()\n"
            "for c in continents:\n"
            "    G.add_node(c)\n"
            "for i in range(len(continents) - 1):\n"
            "    G.add_edge(continents[i], continents[i + 1])\n"
            "plt.figure(figsize=(6, 4))\n"
            "nx.draw_networkx(G, node_size=1200)\n"
            "plt.title('Simple continent relationship graph')\n"
            "plt.axis('off')\n"
            "plt.show()",
            tags=["exercise"],
        ),
        md(
            "## Reflection\n"
            "- Capstone kết hợp: trend + map + graph nhỏ + narrative.\n"
            "- Bản production app nằm trong `solutions/lab10_capstone/streamlit_app/app.py`.\n"
        ),
    ]


def write_apps():
    lab9_app = ROOT / "solutions" / "lab09_chapter9" / "app.py"
    lab9_app.parent.mkdir(parents=True, exist_ok=True)
    lab9_app.write_text(
        'import pandas as pd\n'
        'import plotly.express as px\n'
        'import streamlit as st\n'
        'from pathlib import Path\n\n'
        'st.set_page_config(page_title="Lab09 Solution", layout="wide")\n'
        'st.title("Lab 09 Solution — Data Storytelling")\n'
        'root = Path(__file__).resolve().parents[2]\n'
        'df = pd.read_csv(root / "data" / "gapminder.csv")\n'
        'year = st.slider("Year", int(df.year.min()), int(df.year.max()), 2007)\n'
        'd = df[df.year == year]\n'
        'fig = px.scatter(d, x="gdpPercap", y="lifeExp", color="continent", size="pop", log_x=True)\n'
        'st.plotly_chart(fig, use_container_width=True)\n'
        'st.markdown("Takeaway: GDP per capita có quan hệ thuận với life expectancy, nhưng khác biệt theo khu vực.")\n',
        encoding="utf-8",
    )

    cap_app = ROOT / "solutions" / "lab10_capstone" / "streamlit_app" / "app.py"
    cap_app.parent.mkdir(parents=True, exist_ok=True)
    cap_app.write_text(
        'import pandas as pd\n'
        'import plotly.express as px\n'
        'import streamlit as st\n'
        'from pathlib import Path\n\n'
        'st.set_page_config(page_title="Capstone Solution", layout="wide")\n'
        'st.title("Capstone Solution Dashboard")\n'
        'root = Path(__file__).resolve().parents[3]\n'
        'df = pd.read_csv(root / "data" / "gapminder.csv")\n'
        'continent = st.selectbox("Continent", sorted(df.continent.unique()))\n'
        'd = df[df.continent == continent]\n'
        'fig = px.line(d.groupby("year", as_index=False).agg(lifeExp=("lifeExp", "mean")), x="year", y="lifeExp")\n'
        'st.plotly_chart(fig, use_container_width=True)\n'
        'st.caption("Narrative: tiến bộ life expectancy theo thời gian của từng châu lục.")\n',
        encoding="utf-8",
    )

    cap_readme = ROOT / "solutions" / "lab10_capstone" / "README_capstone.md"
    cap_readme.write_text(
        "# Capstone solution summary\n\n"
        "- Dataset: `data/gapminder.csv`\n"
        "- Main question: xu hướng life expectancy theo thời gian và khác biệt khu vực.\n"
        "- Viz decisions: line (temporal), choropleth (geographic), graph nhẹ (relationship).\n"
        "- Limitation: dữ liệu tổng hợp quốc gia, chưa đi sâu causal inference.\n",
        encoding="utf-8",
    )


def main() -> None:
    write_nb(ROOT / "solutions" / "lab03_chapter3" / "solution.ipynb", lab03_cells())
    write_nb(ROOT / "solutions" / "lab04_chapter4" / "solution.ipynb", lab04_cells())
    write_nb(ROOT / "solutions" / "lab05_chapter5" / "solution.ipynb", lab05_cells())
    write_nb(ROOT / "solutions" / "lab06_chapter6" / "solution.ipynb", lab06_cells())
    write_nb(ROOT / "solutions" / "lab07_chapter7" / "solution.ipynb", lab07_cells())
    write_nb(ROOT / "solutions" / "lab08_chapter8" / "solution.ipynb", lab08_cells())
    write_nb(ROOT / "solutions" / "lab09_chapter9" / "solution.ipynb", lab09_cells())
    write_nb(ROOT / "solutions" / "lab10_capstone" / "solution.ipynb", lab10_cells())
    write_apps()
    print("Wrote solutions for Lab03–10")


if __name__ == "__main__":
    main()

