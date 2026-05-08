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

## `owid_co2_subset.csv`

Bảng panel từ **Our World in Data CO2 dataset** (quốc gia x năm), đã lọc gọn cho lab nâng cao.

- **Nguồn build:** `python ../scripts/download_owid_co2_subset.py`
- **Nguồn upstream:** `owid/co2-data` (GitHub raw CSV)
- **Khoảng thời gian mặc định:** từ năm 1990 trở đi

### Cột chính trong subset

- `country`, `iso_code`, `year`
- `population`, `gdp`
- `co2`, `co2_per_capita`
- `methane`, `nitrous_oxide`
- `energy_per_capita`, `primary_energy_consumption`
- `coal_co2`, `oil_co2`, `gas_co2`
- `temperature_change_from_ghg`, `trade_co2`

### Gợi ý lab

- Color use / sequential-diverging: dùng `co2_per_capita`, `co2_per_capita - global_mean`
- Temporal advanced: heatmap theo `country x year`, lag plot theo từng quốc gia
- Multi-panel/compound figure: kết hợp `gdp`, `co2_per_capita`, `population`
- Uncertainty/risk: CI/band trên trend `co2_per_capita`

Đường dẫn tương đối từ notebook trong `labs/`:

```python
import pandas as pd
from pathlib import Path

def resolve_repo_root() -> Path:
    cwd = Path.cwd().resolve()
    for p in [cwd, *cwd.parents]:
        if (p / "data" / "owid_co2_subset.csv").exists():
            return p
    raise FileNotFoundError("Cannot locate data/owid_co2_subset.csv")

root = resolve_repo_root()
df = pd.read_csv(root / "data" / "owid_co2_subset.csv")
```
