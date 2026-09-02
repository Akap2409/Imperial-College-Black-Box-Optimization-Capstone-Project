"""Generate a concise, portfolio-ready report from experiment outputs."""

from __future__ import annotations

from pathlib import Path

from .data import format_query
from .experiment import ExperimentResult


def write_report(results: list[ExperimentResult], destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Retrospective Optimisation Report",
        "",
        "This report replays the recorded capstone observations using one transparent Gaussian-process surrogate and a UCB acquisition function. It is a retrospective analysis, not a claim that these exact proposals were used in every historical submission.",
        "",
        "| Function | Dim | Best observed output | Proposed next query | Predicted rank | Uncertainty | LOO rank MAE |",
        "| --- | ---: | ---: | --- | ---: | ---: | ---: |",
    ]
    for result in results:
        lines.append(
            f"| {result.function} | {result.dimension} | {result.best_observed_value:.8g} | "
            f"`{format_query(result.proposal)}` | {result.predicted_rank:.3f} | "
            f"{result.predicted_uncertainty:.3f} | {result.loo_rank_mae:.3f} |"
        )
    lines.extend(
        [
            "",
            "## Reading the metrics",
            "",
            "- Lower leave-one-out rank MAE indicates that the small-data surrogate reproduces the relative ordering of observed outcomes more consistently.",
            "- The predicted rank is clipped to the observed [0, 1] ranking scale; it and the uncertainty are not predictions of the original objective value.",
            "- A candidate proposal is evidence for a next experiment, not evidence that the global optimum has been found.",
            "",
        ]
    )
    destination.write_text("\n".join(lines), encoding="utf-8")


def write_weekly_replay(
    rows: list[dict[str, object]],
    destination: Path,
) -> None:
    """Write a chronological no-future-data reconstruction of each decision stage."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Chronological Optimisation Replay",
        "",
        "This report reconstructs what a single transparent UCB workflow would recommend at each recorded stage using only observations available at that time. It deliberately does not use future outputs when producing a recommendation. The recommendations are retrospective comparisons, not replacements for the original portal submissions.",
        "",
    ]
    current_round: int | None = None
    for row in rows:
        round_number = int(row["round"])
        if round_number != current_round:
            current_round = round_number
            lines.extend(
                [
                    f"## After Round {round_number}",
                    "",
                    "| Function | Reconstructed UCB proposal | Actual next recorded query | Actual next output | LOO rank MAE |",
                    "| --- | --- | --- | ---: | ---: |",
                ]
            )
        lines.append(
            f"| {row['function']} | `{row['proposal']}` | `{row['actual_query']}` | "
            f"{float(row['actual_output']):.8g} | {float(row['loo_rank_mae']):.3f} |"
        )
        if row["function"] == "Function 8":
            lines.append("")
    destination.write_text("\n".join(lines), encoding="utf-8")
