# Reproducibility Guide

## Scope

This repository reproduces the final retrospective analysis using the 88 documented query-output pairs in `data/observations.csv`. It does not redistribute course-platform starter files or claim to reconstruct unknown function formulas.

## Environment

The code requires Python 3.10 or later and NumPy. The project metadata is in `pyproject.toml`.

```bash
python -m pip install -e .
```

For tests, install the development extra:

```bash
python -m pip install -e ".[dev]"
```

## Run The Analysis

From the repository root:

```bash
python scripts/run_experiment.py
python scripts/replay_rounds.py
python scripts/generate_figure.py
```

These commands create or update:

- `reports/retrospective_optimisation_report.md`
- `reports/chronological_optimisation_replay.md`
- `figures/optimisation_history.svg`

## Verify The Code

```bash
pytest
```

The tests check data shape, bounded unseen proposals, acquisition output shape, finite surrogate predictions, and protection against future-data leakage in the chronological replay.

## Determinism And Limits

Candidate generation uses fixed per-function random seeds, so repeated runs with the same dependency versions should produce the same report. The analysis is retrospective: it evaluates a consistent final methodology against the documented history. Its recommendations are not proof that the hidden global optima were found.
