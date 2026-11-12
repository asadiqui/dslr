"""pair_plot.py — pair plot / scatter plot matrix of the features.

From this visualization: which features will be used for the logistic regression?

Owner: Abdellah Sadiqui
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from common.dataset import default_dataset, load_csv, numerical_columns, houses
from common.stats import mean, standard_deviation


def feature_separation(rows, column, house_names):
    """Rank features by between-house mean distance relative to spread."""
    groups = []
    for house in house_names:
        data = [
            row[column]
            for row in rows
            if row.get("Hogwarts House") == house
            and isinstance(row.get(column), (int, float))
        ]
        if data:
            groups.append(data)
    if len(groups) < 2:
        return 0.0
    centers = [mean(data) for data in groups]
    overall = mean(centers)
    between = 0.0
    within = 0.0
    for center in centers:
        between += (center - overall) ** 2
    for data in groups:
        within += standard_deviation(data)
    return between / (within + 1e-12)


def selected_features(rows, columns, house_names, limit=6):
    ranked = sorted(
        columns,
        key=lambda column: feature_separation(rows, column, house_names),
        reverse=True,
    )
    return ranked[:limit]


def main() -> int:
    path = sys.argv[1] if len(sys.argv) == 2 else default_dataset()
    if len(sys.argv) > 2:
        print("usage: python visualization/pair_plot.py [dataset.csv]", file=sys.stderr)
        return 1
    try:
        rows = load_csv(path)
        columns = numerical_columns(rows)
        house_names = houses(rows)
        features = selected_features(rows, columns, house_names)
        if not features:
            raise ValueError("dataset needs numerical features and house labels")
    except (OSError, ValueError) as error:
        print("pair_plot: {}".format(error), file=sys.stderr)
        return 1

    frame_rows = []
    for row in rows:
        frame_row = {column: row.get(column) for column in features}
        frame_row["Hogwarts House"] = row.get("Hogwarts House")
        frame_rows.append(frame_row)
    frame = pd.DataFrame(frame_rows).dropna()
    grid = sns.pairplot(frame, vars=features, hue="Hogwarts House", corner=True)
    grid.fig.suptitle("Most useful features by Hogwarts house", y=1.02)
    print("Features selected for regression: {}".format(", ".join(features)))
    plt.show()
    return 0


if __name__ == "__main__":
    main()
