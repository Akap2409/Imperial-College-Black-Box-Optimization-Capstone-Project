"""Load the documented query-output history used in the capstone."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass(frozen=True)
class FunctionDataset:
    """Observed queries and objective values for one unknown function."""

    name: str
    rounds: np.ndarray
    x: np.ndarray
    y: np.ndarray

    @property
    def dimension(self) -> int:
        return int(self.x.shape[1])

    @property
    def best_index(self) -> int:
        return int(np.argmax(self.y))

    @property
    def best_point(self) -> np.ndarray:
        return self.x[self.best_index]

    @property
    def best_value(self) -> float:
        return float(self.y[self.best_index])

    def through_round(self, round_number: int) -> "FunctionDataset":
        """Return only information that was available by the given round."""
        keep = self.rounds <= round_number
        if not np.any(keep):
            raise ValueError(f"No observations are available by round {round_number}.")
        return FunctionDataset(name=self.name, rounds=self.rounds[keep], x=self.x[keep], y=self.y[keep])


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_datasets(path: Path | None = None) -> list[FunctionDataset]:
    """Load all eight functions from the versioned CSV observation history."""
    csv_path = path or project_root() / "data" / "observations.csv"
    grouped: dict[str, list[tuple[int, float, list[float]]]] = {}

    with csv_path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            point = [float(value) for value in row["point"].split("|")]
            grouped.setdefault(row["function"], []).append(
                (int(row["round"]), float(row["output"]), point)
            )

    datasets: list[FunctionDataset] = []
    for name in sorted(grouped, key=lambda value: int(value.split("_")[1])):
        rows = sorted(grouped[name], key=lambda value: value[0])
        datasets.append(
            FunctionDataset(
                name=name.replace("_", " "),
                rounds=np.asarray([row[0] for row in rows], dtype=int),
                y=np.asarray([row[1] for row in rows], dtype=float),
                x=np.asarray([row[2] for row in rows], dtype=float),
            )
        )
    return datasets


def format_query(point: np.ndarray) -> str:
    """Format a point in the course portal's six-decimal query format."""
    return "-".join(f"{value:.6f}" for value in point)
