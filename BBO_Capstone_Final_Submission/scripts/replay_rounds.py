"""Reconstruct weekly optimisation decisions without leaking future observations.

This script is intentionally a replay, not a fabricated history. For each stage,
the surrogate sees only outcomes returned up to that point and produces a fresh
UCB recommendation. The actual next recorded query and outcome are shown only
after the recommendation for comparison.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from bbo_capstone.data import format_query, load_datasets  # noqa: E402
from bbo_capstone.experiment import run_experiment  # noqa: E402
from bbo_capstone.reporting import write_weekly_replay  # noqa: E402


def main() -> None:
    rows: list[dict[str, object]] = []
    for dataset in load_datasets():
        # Three observations are the minimum used for the initial surrogate.
        for round_number in range(3, int(dataset.rounds.max())):
            available = dataset.through_round(round_number)
            actual_next_index = round_number
            result = run_experiment(available, acquisition="ucb")
            rows.append(
                {
                    "round": round_number,
                    "function": dataset.name,
                    "proposal": format_query(result.proposal),
                    "actual_query": format_query(dataset.x[actual_next_index]),
                    "actual_output": float(dataset.y[actual_next_index]),
                    "loo_rank_mae": result.loo_rank_mae,
                }
            )

    rows.sort(key=lambda row: (int(row["round"]), str(row["function"])))
    report_path = ROOT / "reports" / "chronological_optimisation_replay.md"
    write_weekly_replay(rows, report_path)
    print(f"Chronological replay written to: {report_path}")


if __name__ == "__main__":
    main()
