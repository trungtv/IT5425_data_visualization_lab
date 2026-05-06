# Sample datasets (IT5425)

## `gapminder.csv`

Bảng **Gapminder** chuẩn hóa (Plotly mirror): quốc gia × năm — `lifeExp`, `gdpPercap`, `pop`, `continent`, `iso_alpha`, `iso_num`.

- **Nguồn build:** `python ../scripts/download_sample_data.py` (cần internet lần đầu khi generate).
- **Offline:** file CSV đã commit trong repo để lab chạy không cần mạng.

### Gợi ý lab

| Lab | Cách dùng |
|-----|-----------|
| 1–6 | EDA, scatter, bảng, redesign |
| 8 | Choroplet / map (cột `iso_alpha` hoặc lat-lon nếu merge thêm) |
| 9–10 | Dashboard, story theo thời gian (`year`) |

Đường dẫn tương đối từ notebook trong `labs/`:

```python
import pandas as pd
from pathlib import Path
root = Path("..").resolve().parent  # từ labs/labXX → repo root
df = pd.read_csv(root / "data" / "gapminder.csv")
```

Hoặc copy đoạn trên và chỉnh `root` cho đúng chỗ bạn mở notebook.
