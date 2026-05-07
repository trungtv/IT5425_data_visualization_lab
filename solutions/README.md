# Solutions (GV)

Thư mục này chứa **bản lời giải đầy đủ** (đã chạy end-to-end) cho từng lab, tổ chức theo phase.

- Không dùng cho sinh viên (tránh lộ đáp án).
- Bản `labs/` (exercise) được **generate** từ `solutions/` bằng script `scripts/make_exercises.py`.

## Quy ước

- Mỗi lab có một notebook `solution.ipynb`.
- Các cell cần “đục lỗ” trong bản exercise sẽ có tag `exercise` trong metadata.
- Cấu trúc thư mục theo phase tương ứng với `labs/`.

## Build nhanh

```bash
.venv/bin/python scripts/build_solutions_01_02.py
.venv/bin/python scripts/build_solutions_03_10.py
.venv/bin/python scripts/make_exercises.py
```
