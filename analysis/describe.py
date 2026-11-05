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


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python analysis/describe.py <dataset.csv>", file=sys.stderr)
        return 1
    # TODO: load the CSV, keep numerical columns, compute stats by hand, print the table
    raise NotImplementedError


if __name__ == "__main__":
    sys.exit(main())
