# Sequential Black-Box Optimisation Under Severe Data Constraints

This repository documents an independent Black-Box Optimisation (BBO) capstone project completed as part of Imperial College Business School's Professional Certificate in Machine Learning and Artificial Intelligence. The project investigates how to maximise eight unknown functions when their formulas, gradients, and full response surfaces are unavailable.

## In Plain English

Imagine trying to tune an expensive system when you can test only one setting at a time and only receive a score afterwards. You cannot see the rules behind the system or try every possible combination. This project records how I used the limited feedback from each test to choose the next setting more carefully. I began by exploring different areas, then focused more effort on regions that appeared promising. The accompanying code turns that learning process into a transparent optimisation workflow that can be rerun, inspected, and improved.

## Project Objective

The capstone contains eight independent maximisation problems with input spaces from 2 to 8 dimensions. Every coordinate must be inside `[0, 1]`, and the evaluation budget is deliberately small. The technical objective is not to claim a guaranteed global optimum; it is to make principled, reproducible sequential decisions under uncertainty.

The final codebase provides a retrospective, reproducible surrogate-modelling analysis of the documented query history. It does not rewrite history or claim that a single final model generated every course submission.

## Technical Approach

The reusable workflow uses one small Gaussian-process surrogate per function. It keeps the modelling assumptions deliberately conservative because only 11 recorded observations are available for each function.

1. Load the versioned query-output history from `data/observations.csv`.
2. Rank-normalise outputs within each function so the model is stable across very different objective scales.
3. Fit a Gaussian-process surrogate with a fixed RBF kernel and small numerical noise term.
4. Generate a mixed candidate pool: global uniform samples plus local perturbations around the three best observed points.
5. Score candidates with UCB, Expected Improvement, or posterior variance.
6. Report a reproducible proposed query and leave-one-out rank error for each function.

This makes the exploration-exploitation trade-off explicit:

- `UCB` balances predicted performance and uncertainty.
- `EI` prioritises candidates expected to beat the current best estimate.
- `variance` performs pure exploration where the surrogate is uncertain.

## Repository Structure

```text
.
├── data/
│   └── observations.csv              # Documented 11-round query-output history
├── src/bbo_capstone/
│   ├── data.py                       # Data loading and query formatting
│   ├── surrogate.py                  # NumPy Gaussian process and acquisitions
│   ├── experiment.py                 # Candidate search and LOO stability checks
│   └── reporting.py                  # Markdown report generation
├── scripts/run_experiment.py         # Reproducible command-line workflow
├── scripts/replay_rounds.py           # No-future-data chronological replay
├── scripts/generate_figure.py         # Dependency-free SVG figure generator
├── tests/test_core.py                # Core behavioural tests
├── reports/                          # Generated result summaries
├── BBO_Capstone_Demo.ipynb           # Reviewer-friendly walkthrough
├── DATASHEET.md                      # Dataset documentation
├── MODEL_CARD.md                     # Model documentation and limitations
├── REPRODUCIBILITY.md                 # Environment and verification guide
├── REFERENCES.md                      # Academic and software references
├── SUBMISSION_CHECKLIST.md             # Final GitHub submission checks
└── BBO_capstone_presentation_completed.pdf
```

## Quick Start

The core workflow requires only NumPy.

```bash
python -m pip install -e .
python scripts/run_experiment.py
python scripts/replay_rounds.py
```

Choose an alternative acquisition function:

```bash
python scripts/run_experiment.py --acquisition ei
python scripts/run_experiment.py --acquisition variance
```

Run the test suite after installing the optional development dependency:

```bash
python -m pip install -e ".[dev]"
pytest
```

The main script writes [reports/retrospective_optimisation_report.md](reports/retrospective_optimisation_report.md), including proposed next queries, uncertainty, and leave-one-out rank error for all eight functions. The replay script writes [reports/chronological_optimisation_replay.md](reports/chronological_optimisation_replay.md), which documents each stage using only data available at that point and compares the reconstructed recommendation with the next actual recorded result.

## Data

The included dataset contains 88 observed query-output pairs: 11 recorded rounds for each of eight unknown functions. The functions have dimensions 2, 2, 3, 4, 4, 5, 6, and 8. Course-provided raw files are not re-hosted beyond the documented observations because their distribution is subject to course policy.

The data is adaptive rather than randomly sampled. Later queries are informed by previous outputs, which is necessary for optimisation but introduces selection bias. See [DATASHEET.md](DATASHEET.md) for motivation, collection, uses, and constraints.

## Evaluation And Limitations

The central performance signal is the best observed objective value, because each function is a maximisation task. The code also calculates leave-one-out rank mean absolute error as a small-data sanity check. It assesses whether the surrogate reproduces the relative ordering of observed values; it is not a proof of global-optimum discovery.

Important limitations remain:

- Eleven observations per function cannot identify a complex high-dimensional surface reliably.
- Rank normalisation preserves ordering but does not preserve output magnitude; predicted ranks are clipped to the observed `[0, 1]` range to avoid implausible extrapolation.
- A fixed kernel avoids unstable tuning, but may underfit or overfit a particular function.
- Candidate proposals should be treated as experimental recommendations, not factual outcomes.

See [MODEL_CARD.md](MODEL_CARD.md) for intended use, model details, limitations, and responsible interpretation.

## Presentation Materials

- [Notebook walkthrough](BBO_Capstone_Demo.ipynb)
- [Datasheet](DATASHEET.md)
- [Model card](MODEL_CARD.md)
- [Reproducibility guide](REPRODUCIBILITY.md)
- [References](REFERENCES.md)
- [Submission checklist](SUBMISSION_CHECKLIST.md)
- [Optimisation history figure](figures/optimisation_history.svg)
- [Capstone presentation](BBO_capstone_presentation_completed.pdf)

## Reproducibility Notes

The workflow fixes random seeds for every function, keeps input data in a human-readable CSV, and avoids hidden cloud services or proprietary packages. This repository is intended as a transparent portfolio artifact demonstrating sequential experimentation, uncertainty-aware optimisation, and responsible reporting with incomplete information.
