"""describe.py — display statistics for every numerical feature of a dataset.

Usage: python analysis/describe.py datasets/dataset_train.csv

Rows to display: Count, Mean, Std, Min, 25%, 50%, 75%, Max.
Every statistic must be computed by hand (no describe(), mean(), std(), min(), max(), percentile()...).

Bonus: add more statistical fields.

Owner: Abdellah Sadiqui
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from common.dataset import load_csv, numerical_columns, values
from common.stats import describe


def main() -> int:
    if len(sys.argv) not in (2, 3) or (len(sys.argv) == 3 and sys.argv[2] != "--bonus"):
        print(
            "usage: python analysis/describe.py <dataset.csv> [--bonus]",
            file=sys.stderr,
        )
        return 1
    try:
        rows = load_csv(sys.argv[1])
        columns = numerical_columns(rows)
        if not columns:
            raise ValueError("dataset contains no numerical features")
        statistics = {column: describe(values(rows, column)) for column in columns}
    except (OSError, ValueError) as error:
        print("describe: {}".format(error), file=sys.stderr)
        return 1

    fields = ["Count", "Mean", "Std", "Min", "25%", "50%", "75%", "Max"]
    if len(sys.argv) == 3:
        fields.extend(["Variance", "IQR"])
    width = len(fields[0])
    for field in fields[1:]:
        if len(field) > width:
            width = len(field)
    print("{:<{}} {}".format("", width, " ".join("{:>14}".format(column) for column in columns)))
    for field in fields:
        rendered = " ".join(
            "{:>14.6f}".format(statistics[column][field]) for column in columns
        )
        print("{:<{}} {}".format(field, width, rendered))
    return 0


if __name__ == "__main__":
    sys.exit(main())
