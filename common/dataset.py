"""CSV loading and feature-selection helpers for the analysis scripts."""

import csv
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence


Row = Dict[str, object]


def load_csv(path: str) -> List[Row]:
    """Load a CSV while converting non-empty numeric cells to ``float``."""
    csv_path = Path(path)
    if not csv_path.is_file():
        raise FileNotFoundError("dataset not found: {}".format(path))

    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError("dataset has no header: {}".format(path))
        rows: List[Row] = []
        for raw_row in reader:
            row: Row = {}
            for name, value in raw_row.items():
                if value is None or value.strip() == "":
                    row[name] = None
                    continue
                try:
                    row[name] = float(value)
                except ValueError:
                    row[name] = value
            rows.append(row)
    return rows


def numerical_columns(
    rows: Sequence[Row], excluded: Iterable[str] = ("Index",)
) -> List[str]:
    """Return columns whose non-missing values are all numeric."""
    if not rows:
        return []
    excluded_set = set(excluded)
    columns = list(rows[0].keys())
    numeric: List[str] = []
    for column in columns:
        if column in excluded_set:
            continue
        has_value = False
        is_numeric = True
        for row in rows:
            value = row.get(column)
            if value is None:
                continue
            has_value = True
            if not isinstance(value, (int, float)):
                is_numeric = False
                break
        if has_value and is_numeric:
            numeric.append(column)
    return numeric


def values(rows: Sequence[Row], column: str) -> List[float]:
    """Return finite numeric values for one column."""
    result: List[float] = []
    for row in rows:
        value = row.get(column)
        if isinstance(value, (int, float)):
            result.append(float(value))
    return result


def houses(rows: Sequence[Row]) -> List[str]:
    """Return house labels in first-seen order, excluding missing labels."""
    result: List[str] = []
    for row in rows:
        house = row.get("Hogwarts House")
        if isinstance(house, str) and house and house not in result:
            result.append(house)
    return result


def default_dataset(name: str = "dataset_train.csv") -> str:
    """Resolve a dataset relative to the repository root."""
    return str(Path(__file__).resolve().parent.parent / "datasets" / name)


def group_values(rows: Sequence[Row], column: str, house: str) -> List[float]:
    """Return numeric values for one feature and one Hogwarts house."""
    return values(
        [row for row in rows if row.get("Hogwarts House") == house],
        column,
    )
