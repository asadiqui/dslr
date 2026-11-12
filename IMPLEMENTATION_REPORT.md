# DSLR Project Implementation Report

## 1. Scope and requirements addressed

The documented work split assigns Abdellah Sadiqui:

- Data analysis: `analysis/describe.py`
- Data visualization:
  - `visualization/histogram.py`
  - `visualization/scatter_plot.py`
  - `visualization/pair_plot.py`
- Optional bonus: additional statistical fields in `describe.py`

Logistic-regression training and prediction belong to Hiba Chokri and were
deliberately left untouched. The implementation follows `dslr.txt` by:

- accepting the training CSV for analysis;
- identifying numerical features without treating `Index` as a feature;
- computing required descriptive statistics without pandas/scikit-learn
  aggregation helpers;
- producing the three requested visualizations;
- printing the answer inferred by each visualization;
- handling blank cells and non-numeric metadata safely.

The optional `--bonus` mode adds `Variance` and `IQR` to the required
statistics table. The bonus gradient-descent work remains Hiba's scope and is
not included here.

## 2. Implementation plan and execution order

The work was executed in dependency order:

1. Read `dslr.txt` and `README.md`, then inspect the repository, datasets,
   dependencies, branch, and commit history.
2. Build shared CSV and feature-selection helpers in
   [common/dataset.py](common/dataset.py).
3. Build hand-written statistics in [common/stats.py](common/stats.py).
4. Implement `describe.py` on top of those shared helpers.
5. Implement the histogram, scatter plot, and pair plot scripts.
6. Correct edge cases found during review, including missing-value pairing and
   forbidden built-in aggregate usage.
7. Run compilation, smoke tests, CLI checks, headless visualization checks,
   and whitespace validation.
8. Commit only the verified Abdellah-scope files.

This order ensures that all scripts use one consistent interpretation of CSV
values and missing data instead of duplicating parsing logic.

## 3. Completed tasks and reasoning

### 3.1 Shared dataset loading

[common/dataset.py](common/dataset.py) provides the common data path:

1. `load_csv()` uses `csv.DictReader` to preserve column names.
2. Empty cells become `None`.
3. Non-empty values that can be parsed as numbers become `float`; names,
   dates, houses, and hand information remain strings.
4. `numerical_columns()` examines each column and keeps columns whose
   non-missing values are numeric, excluding `Index`.
5. `values()` extracts numeric values for a feature.
6. `houses()` returns distinct house labels in first-seen order.
7. `group_values()` filters a feature by Hogwarts house.
8. `default_dataset()` resolves `datasets/dataset_train.csv` relative to the
   repository, so the scripts work when launched from the project root.

This shared layer connects every analysis script to the same input contract.
It also avoids accidentally using names, dates, or house labels as numerical
features.

### 3.2 Hand-written statistics

[common/stats.py](common/stats.py) implements:

- arithmetic mean using an explicit loop;
- sample variance and standard deviation;
- linearly interpolated quantiles;
- minimum and maximum using explicit comparisons;
- interquartile range.

The code intentionally does not use `describe()`, `mean()`, `std()`,
`min()`, `max()`, `percentile()`, or equivalent statistics helpers from a
third-party library. Sorting is used only to implement the quantile definition
directly.

### 3.3 Descriptive analysis

[analysis/describe.py](analysis/describe.py) loads the requested CSV, obtains
the numerical columns, calculates each column's statistics, and prints a
table with:

`Count`, `Mean`, `Std`, `Min`, `25%`, `50%`, `75%`, and `Max`.

Passing `--bonus` additionally prints `Variance` and `IQR`. Invalid argument
counts, missing files, empty datasets, and datasets without numerical
features produce an error message and a non-zero exit status.

### 3.4 Histogram

[visualization/histogram.py](visualization/histogram.py) creates one subplot
per numerical course and overlays one histogram per house. It also computes a
simple homogeneity score from variation in house means and standard deviations.
The course with the lowest score is printed as the answer to the subject's
question.

The current training data produced:

`Most homogeneous course: Care of Magical Creatures`

### 3.5 Scatter plot and code connection

[visualization/scatter_plot.py](visualization/scatter_plot.py) answers which
two features are similar:

1. `main()` chooses the user-provided dataset or the default training dataset.
2. `load_csv()` supplies typed row dictionaries from the shared dataset layer.
3. `numerical_columns()` supplies the candidate feature names.
4. `most_similar_pair()` checks every distinct feature pair.
5. `paired_values()` is called for each pair and keeps only rows where both
   values are numeric. This is important because independently filtering two
   columns could misalign observations when one value is missing.
6. `correlation()` computes Pearson correlation manually:
   - calculate both means through `common.stats.mean`;
   - accumulate centered cross-products;
   - accumulate each centered sum of squares;
   - divide by the product of the two norms.
7. `most_similar_pair()` compares the absolute correlation, so both strong
   positive and strong negative relationships count as similar.
8. `main()` plots the selected pair with Matplotlib and prints the feature
   names and correlation score.

The plot is therefore connected to the same parsed rows and numerical-feature
selection used by `describe.py`; it does not independently reinterpret the
CSV. On the supplied training data it reported:

`Most similar features: Astronomy and Defense Against the Dark Arts
(correlation 1.0000)`

The implementation returns a clear error for invalid argument counts, missing
files, or datasets with fewer than two numerical features.

### 3.6 Pair plot

[visualization/pair_plot.py](visualization/pair_plot.py) ranks features by
between-house mean separation relative to within-house spread, keeps the top
six, and renders a Seaborn pair plot colored by `Hogwarts House`. It prints
the selected feature names so the visual analysis has a reproducible textual
result.

The current training data selected:

`Astronomy, Muggle Studies, Ancient Runes, Flying, Transfiguration, Charms`

Pandas and Seaborn are used here for plotting/data-frame presentation only;
the statistical ranking itself is hand-written.

## 4. Important technical decisions and alternatives

- **Standard-library CSV parsing instead of pandas loading:** this keeps
  parsing transparent and respects the subject's restriction against
  heavy-lifting analysis helpers.
- **Shared helpers instead of duplicated parsing:** this prevents the three
  visualizations and `describe.py` from disagreeing about missing values or
  numeric columns.
- **Sample standard deviation:** the statistics layer uses the conventional
  sample denominator (`n - 1`), matching typical descriptive-statistics
  output.
- **Linear quantile interpolation:** quartiles use the position
  `p * (n - 1)`, which gives stable results for both even and odd sample sizes.
- **Absolute correlation:** similarity includes either orientation of a linear
  relationship, not only positive correlation.
- **Headless-safe execution:** plots still call `plt.show()` for normal
  interactive use, while `MPLBACKEND=Agg` permits automated validation without
  a display.
- **No regression integration changes:** the visualization scripts report
  candidate features but do not modify Hiba's training or prediction scripts.

## 5. Tests and results

The following checks were run successfully:

1. Python compilation:
   `python -m py_compile` on all changed Python modules.
2. Required describe command:
   `python analysis/describe.py datasets/dataset_train.csv`
   produced the eight required statistic rows.
3. Bonus describe command:
   `python analysis/describe.py datasets/dataset_train.csv --bonus`
   produced `Variance` and `IQR`.
4. Histogram:
   `MPLBACKEND=Agg python visualization/histogram.py`
   completed and printed the homogeneous course.
5. Scatter plot:
   `MPLBACKEND=Agg python visualization/scatter_plot.py`
   completed and printed the most similar pair.
6. Pair plot:
   `MPLBACKEND=Agg python visualization/pair_plot.py`
   completed and printed the selected features.
7. Statistics smoke test:
   verified 1–4 mean, quartiles, row count, and exclusion of `Index`.
8. Error handling:
   invoking `describe.py` without its required path returned status 1 and a
   usage message.
9. `git diff --check` passed.
10. A grep review confirmed no forbidden aggregate call remained in executable
    analysis code.

The headless plot checks emit the expected Matplotlib warning that an
interactive canvas cannot be shown; this is an environment warning, not a
script failure.

## 6. Files created, modified, or deleted

### Created

- [common/stats.py](common/stats.py)
- [IMPLEMENTATION_REPORT.md](IMPLEMENTATION_REPORT.md) (this report)

### Modified

- [common/dataset.py](common/dataset.py)
- [analysis/describe.py](analysis/describe.py)
- [visualization/histogram.py](visualization/histogram.py)
- [visualization/scatter_plot.py](visualization/scatter_plot.py)
- [visualization/pair_plot.py](visualization/pair_plot.py)

### Deleted

None.

The regression files were intentionally not modified. A pre-existing
`.gitignore` worktree modification was also left untouched.

## 7. Git commits and push status

Created local commit:

- `807979c` — `Implement data analysis and visualization`

The commit includes the verified analysis and visualization implementation and
the required Copilot co-author trailer. The push to `origin/main` was
attempted but did not succeed because GitHub credentials were unavailable in
the non-interactive environment. The local branch is therefore one commit
ahead of `origin/main`.

## 8. Remaining work, limitations, and recommendations

- Hiba still needs to implement and validate logistic-regression training and
  prediction, including the required 98% test accuracy target.
- The visualization scripts call `plt.show()` and do not save image files;
  this matches the subject's requirement to display visualizations. A
  future presentation workflow could add an optional output path.
- The homogeneity and feature-separation scores are explicit heuristics for
  answering exploratory questions, not classifier-training metrics.
- The pair plot currently limits itself to six features to keep rendering
  readable; the full numerical feature set remains available through the
  shared loader.
- Before submission, authenticate GitHub and push commit `807979c`, then
  integrate and validate the teammate's regression work without overwriting
  either contributor's scope.
