"""logreg_predict.py — predict the Hogwarts house of every student in the test set.

Usage: python regression/logreg_predict.py datasets/dataset_test.csv weights.json
Output: houses.csv, formatted exactly as "Index,Hogwarts House"

Owner: Hiba Chokri
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))


def main() -> None:
    # TODO: load weights, predict, write houses.csv
    raise NotImplementedError


if __name__ == "__main__":
    main()
