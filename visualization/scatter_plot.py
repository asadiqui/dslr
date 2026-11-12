"""scatter_plot.py — what are the two features that are similar?

Owner: Abdellah Sadiqui
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import matplotlib.pyplot as plt

from common.dataset import default_dataset, load_csv, numerical_columns, values
from common.stats import mean


def paired_values(rows, left, right):
    pairs = []
    for row in rows:
        first = row.get(left)
        second = row.get(right)
        if isinstance(first, (int, float)) and isinstance(second, (int, float)):
            pairs.append((float(first), float(second)))
    return [pair[0] for pair in pairs], [pair[1] for pair in pairs]


def correlation(first, second):
    if len(first) != len(second) or not first:
        return 0.0
    first_mean = mean(first)
    second_mean = mean(second)
    numerator = 0.0
    first_squared = 0.0
    second_squared = 0.0
    for left, right in zip(first, second):
        left_delta = left - first_mean
        right_delta = right - second_mean
        numerator += left_delta * right_delta
        first_squared += left_delta * left_delta
        second_squared += right_delta * right_delta
    denominator = (first_squared * second_squared) ** 0.5
    return numerator / denominator if denominator else 0.0


def most_similar_pair(rows, columns):
    best_pair = (columns[0], columns[1])
    best_score = -1.0
    for left_index, left in enumerate(columns):
        for right in columns[left_index + 1 :]:
            first, second = paired_values(rows, left, right)
            score = abs(correlation(first, second))
            if score > best_score:
                best_pair = (left, right)
                best_score = score
    return best_pair, best_score


def main() -> int:
    path = sys.argv[1] if len(sys.argv) == 2 else default_dataset()
    if len(sys.argv) > 2:
        print("usage: python visualization/scatter_plot.py [dataset.csv]", file=sys.stderr)
        return 1
    try:
        rows = load_csv(path)
        columns = numerical_columns(rows)
        if len(columns) < 2:
            raise ValueError("dataset needs at least two numerical features")
        (left, right), score = most_similar_pair(rows, columns)
    except (OSError, ValueError) as error:
        print("scatter_plot: {}".format(error), file=sys.stderr)
        return 1

    figure, axis = plt.subplots(figsize=(9, 7))
    first, second = paired_values(rows, left, right)
    axis.scatter(first, second, alpha=0.55, s=14)
    axis.set_xlabel(left)
    axis.set_ylabel(right)
    axis.set_title("Most similar features")
    print("Most similar features: {} and {} (correlation {:.4f})".format(left, right, score))
    figure.tight_layout()
    plt.show()
    return 0


if __name__ == "__main__":
    sys.exit(main())
