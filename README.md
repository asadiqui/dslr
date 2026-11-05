# DSLR — Data Science × Logistic Regression

*Harry Potter and the Data Scientist*: recreate the Sorting Hat with a one-vs-all logistic regression classifier.

Target: at least **98% accuracy** on `datasets/dataset_test.csv` (scikit-learn `accuracy_score`).

## Layout

```
analysis/
  describe.py            Data analysis: describe all numerical features
visualization/
  histogram.py           Which course has a homogeneous score distribution across houses?
  scatter_plot.py        Which two features are similar?
  pair_plot.py           Which features to use for the regression?
regression/
  logreg_train.py        Train one-vs-all logistic regression (gradient descent) -> weights file
  logreg_predict.py      Predict houses for the test set -> houses.csv
common/                  Code shared by the parts above (dataset loading, hand-written stats)
datasets/
  dataset_train.csv      training data (with Hogwarts House)
  dataset_test.csv       test data (house column empty)
```

## Usage

Run everything from the repo root:

```
python analysis/describe.py datasets/dataset_train.csv
python visualization/histogram.py
python visualization/scatter_plot.py
python visualization/pair_plot.py
python regression/logreg_train.py datasets/dataset_train.csv
python regression/logreg_predict.py datasets/dataset_test.csv weights.json
```

`houses.csv` must be formatted exactly as:

```
Index,Hogwarts House
0,Gryffindor
1,Hufflepuff
...
```

## Rules to keep in mind

- No helper that does the heavy lifting: no `describe()`, and no built-in `count`, `mean`, `std`, `min`, `max`, `percentile` and the like. Implement them by hand.
- The bonus part is only assessed if the mandatory part is perfect.

## Split of work

| Part | Owner |
|------|-------|
| Data analysis and visualization (`describe`, `histogram`, `scatter_plot`, `pair_plot`) | Abdellah Sadiqui |
| Logistic regression (`logreg_train`, `logreg_predict`) | Hiba Chokri |
| Bonus: more statistical fields in `describe.py` | Abdellah Sadiqui |
| Bonus: stochastic and/or mini-batch gradient descent | Hiba Chokri |
