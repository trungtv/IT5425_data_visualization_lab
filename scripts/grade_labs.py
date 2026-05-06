#!/usr/bin/env python3
"""Strict autograde checks for IT5425 labs."""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

import nbformat

LAB_COUNT = 10
TODO_PATTERN = re.compile(r"\bTODO\b", re.IGNORECASE)


def execute_notebook(py: Path, nb_path: Path, out_dir: Path, timeout: int) -> tuple[bool, str]:
    out_file = out_dir / f"{nb_path.stem}.executed.ipynb"
    cmd = [
        str(py),
        "-m",
        "jupyter",
        "nbconvert",
        "--to",
        "notebook",
        "--execute",
        str(nb_path),
        "--output",
        out_file.name,
        "--output-dir",
        str(out_dir),
        f"--ExecutePreprocessor.timeout={timeout}",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        return False, (proc.stdout + "\n" + proc.stderr).strip()
    return True, str(out_file)


def non_empty_code_outputs(nb: nbformat.NotebookNode) -> int:
    cnt = 0
    for cell in nb.cells:
        if cell.cell_type == "code" and cell.outputs:
            cnt += 1
    return cnt


def has_unresolved_todo(nb: nbformat.NotebookNode) -> bool:
    for cell in nb.cells:
        src = "".join(cell.source if isinstance(cell.source, list) else [cell.source])
        if TODO_PATTERN.search(src):
            return True
    return False


def reflection_length(nb: nbformat.NotebookNode) -> int:
    joined = []
    in_reflect = False
    for cell in nb.cells:
        if cell.cell_type != "markdown":
            continue
        src = "".join(cell.source if isinstance(cell.source, list) else [cell.source])
        if "Reflection" in src:
            in_reflect = True
            joined.append(src)
            continue
        if in_reflect:
            joined.append(src)
    text = "\n".join(joined)
    text = text.replace("Họ tên / MSSV:", "").strip()
    return len(text)


def check_streamlit_lab9(path: Path) -> list[str]:
    src = path.read_text(encoding="utf-8")
    errs: list[str] = []
    if "st.plotly_chart(" not in src:
        errs.append("Lab09 app thiếu st.plotly_chart.")
    if "st.slider(" not in src and "st.selectbox(" not in src and "st.multiselect(" not in src:
        errs.append("Lab09 app thiếu widget tương tác (slider/selectbox/multiselect).")
    if TODO_PATTERN.search(src):
        errs.append("Lab09 app còn TODO.")
    return errs


def check_capstone_files(root: Path) -> list[str]:
    errs: list[str] = []
    capstone_readme = root / "labs" / "lab10_capstone" / "README_capstone.md"
    if not capstone_readme.exists():
        errs.append("Thiếu labs/lab10_capstone/README_capstone.md")
    else:
        txt = capstone_readme.read_text(encoding="utf-8")
        if "TODO" in txt or "Thành viên / MSSV:" in txt:
            errs.append("README_capstone.md chưa điền đầy đủ.")
    capstone_app = root / "labs" / "lab10_capstone" / "streamlit_app" / "app.py"
    src = capstone_app.read_text(encoding="utf-8")
    if TODO_PATTERN.search(src):
        errs.append("Capstone streamlit_app/app.py còn TODO.")
    return errs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--execute", action="store_true", help="Execute notebooks before grading."
    )
    parser.add_argument(
        "--timeout", type=int, default=240, help="Notebook execute timeout seconds."
    )
    parser.add_argument(
        "--python", default=str(Path(".venv/bin/python")), help="Python executable path."
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    labs = root / "labs"
    out_dir = root / ".nbexec_grade"
    out_dir.mkdir(exist_ok=True)

    errors: list[str] = []
    notebook_targets = [labs / f"lab{i:02d}_chapter{i}" / f"lab{i:02d}.ipynb" for i in range(1, 10)]
    notebook_targets.append(labs / "lab10_capstone" / "lab10.ipynb")

    for nb_path in notebook_targets:
        if not nb_path.exists():
            errors.append(f"Thiếu notebook: {nb_path.relative_to(root)}")
            continue

        target_path = nb_path
        if args.execute:
            ok, msg = execute_notebook(Path(args.python), nb_path, out_dir, args.timeout)
            if not ok:
                errors.append(f"Execute fail {nb_path.relative_to(root)}:\n{msg}")
                continue
            target_path = Path(msg)

        nb = nbformat.read(target_path, as_version=4)
        out_count = non_empty_code_outputs(nb)
        if out_count < 1:
            errors.append(f"{nb_path.relative_to(root)}: chưa có output code cell nào.")
        if has_unresolved_todo(nb):
            errors.append(f"{nb_path.relative_to(root)}: còn TODO trong notebook.")
        if reflection_length(nb) < 80:
            errors.append(f"{nb_path.relative_to(root)}: phần Reflection quá ngắn (<80 ký tự).")

    errors.extend(check_streamlit_lab9(labs / "lab09_chapter9" / "app.py"))
    errors.extend(check_capstone_files(root))

    if errors:
        print("AUTOGRADE FAIL")
        for i, err in enumerate(errors, start=1):
            print(f"{i:02d}. {err}")
        return 1

    print(f"AUTOGRADE PASS — validated {LAB_COUNT} labs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
