"""Run the reproducible BBO retrospective experiment from the repository root."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from bbo_capstone.data import format_query, load_datasets  # noqa: E402
from bbo_capstone.experiment import run_experiment  # noqa: E402
from bbo_capstone.reporting import write_report  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the BBO capstone retrospective optimisation workflow.")
    parser.add_argument("--acquisition", choices=("ucb", "ei", "variance"), default="ucb")
    args = parser.parse_args()

    results = [run_experiment(dataset, acquisition=args.acquisition) for dataset in load_datasets()]
    report_path = ROOT / "reports" / "retrospective_optimisation_report.md"
    write_report(results, report_path)

    print("BBO retrospective experiment")
    print("=" * 30)
    for result in results:
        print(f"{result.function}: {format_query(result.proposal)}")
    print(f"\nReport written to: {report_path}")


if __name__ == "__main__":
    main()
