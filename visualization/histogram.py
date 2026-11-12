"""histogram.py — which Hogwarts course has a homogeneous score distribution between all four houses?

Owner: Abdellah Sadiqui
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import matplotlib.pyplot as plt

from common.dataset import default_dataset, group_values, houses, load_csv, numerical_columns
from common.stats import mean, standard_deviation


def homogeneity_score(rows, column, house_names):
    """Compare house distributions using their means and standard deviations."""
    distributions = [group_values(rows, column, house) for house in house_names]
    distributions = [data for data in distributions if data]
    if not distributions:
        return float("inf")
    centers = [mean(data) for data in distributions]
    spreads = [standard_deviation(data) for data in distributions]
    center = mean(centers)
    spread = mean(spreads)
    center_error = 0.0
    spread_error = 0.0
    for value in centers:
        center_error += (value - center) ** 2
    for value in spreads:
        spread_error += (value - spread) ** 2
    scale = abs(center) + abs(spread) + 1.0
    return (center_error + spread_error) / scale


def main() -> int:
    path = sys.argv[1] if len(sys.argv) == 2 else default_dataset()
    if len(sys.argv) > 2:
        print("usage: python visualization/histogram.py [dataset.csv]", file=sys.stderr)
        return 1
    try:
        rows = load_csv(path)
        columns = numerical_columns(rows)
        house_names = houses(rows)
        if not columns or not house_names:
            raise ValueError("dataset needs numerical features and house labels")
        best = columns[0]
        best_score = homogeneity_score(rows, best, house_names)
        for column in columns[1:]:
            score = homogeneity_score(rows, column, house_names)
            if score < best_score:
                best = column
                best_score = score
    except (OSError, ValueError) as error:
        print("histogram: {}".format(error), file=sys.stderr)
        return 1

    figure, axes = plt.subplots(4, 4, figsize=(16, 13))
    flat_axes = axes.flat
    for index, column in enumerate(columns):
        axis = flat_axes[index]
        for house in house_names:
            data = group_values(rows, column, house)
            if data:
                axis.hist(data, bins=20, alpha=0.45, label=house)
        axis.set_title(column)
        axis.set_xlabel("Score")
        axis.set_ylabel("Students")
    for axis in list(flat_axes)[len(columns):]:
        axis.set_visible(False)
    handles, labels = flat_axes[0].get_legend_handles_labels()
    if handles:
        figure.legend(handles, labels, loc="upper right")
    figure.suptitle("Score distributions by Hogwarts house")
    figure.tight_layout()
    print("Most homogeneous course: {}".format(best))
    plt.show()
    return 0


if __name__ == "__main__":
    sys.exit(main())
