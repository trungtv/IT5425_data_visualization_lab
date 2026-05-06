# IT5425 — Data Visualization Lab

Thực hành đi kèm giáo trình *Data Visualization* (`related/english/`). Mỗi lab bám một chương; xem chi tiết trong [`labs/README.md`](labs/README.md).

## Môi trường

### pip / venv

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m ipykernel install --user --name=it5425 --display-name="Python (IT5425)"
```

### Conda / Mamba

```bash
mamba env create -f environment.yml   # hoặc: conda env create -f environment.yml
conda activate it5425-lab
python -m ipykernel install --user --name=it5425 --display-name="Python (IT5425)"
```

Mở Jupyter và chọn kernel **Python (IT5425)**.

## Dữ liệu mẫu

- [`data/gapminder.csv`](data/gapminder.csv) — dùng xuyên labs (xem [`data/README.md`](data/README.md)).
- Tạo lại từ Plotly: `python scripts/download_sample_data.py`

## Kiểm tra notebook (tùy chọn)

```bash
pip install -r requirements-dev.txt   # ruff
python scripts/check_notebooks.py
ruff check scripts/ labs/lab09_chapter9/app.py labs/lab10_capstone/streamlit_app/app.py
```

CI: workflow [`.github/workflows/lab-ci.yml`](.github/workflows/lab-ci.yml) (push/PR).

## Autograde cứng (khi chấm bài)

```bash
# Chạy chấm strict trên notebook đã nộp (không execute lại)
python scripts/grade_labs.py

# Chạy execute rồi chấm (khuyến nghị trước khi thu bài)
python scripts/grade_labs.py --execute --python .venv/bin/python --timeout 240
```

Script `grade_labs.py` kiểm tra tối thiểu:
- Mỗi lab có output code cell thực tế
- Không còn TODO trong notebook
- Reflection có nội dung đủ dài
- Lab 09 có thành phần tương tác Streamlit
- Lab 10 có `README_capstone.md` đã điền và app không còn TODO

## Cấu trúc

- `labs/lab01_chapter1/` … `labs/lab09_chapter9/` — bài tuần.
- `labs/lab10_capstone/` — đồ án cuối.
- `labs/RUBRIC.md` — tiêu chí chấm thống nhất.

## Tài liệu tham khảo

Nội dung lý thuyết: thư mục `related/english/` ( các file `chapter*.tex` ).
