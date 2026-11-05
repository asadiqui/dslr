"""logreg_train.py — train a one-vs-all logistic regression with gradient descent.

Usage: python regression/logreg_train.py datasets/dataset_train.csv
Output: a weights file used by logreg_predict.py

Bonus: stochastic gradient descent and/or mini-batch gradient descent.

Owner: Hiba Chokri
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))


def main() -> None:
    # TODO: one-vs-all training (one model per house), write weights to a file
    raise NotImplementedError


if __name__ == "__main__":
    main()
