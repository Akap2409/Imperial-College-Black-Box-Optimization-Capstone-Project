"""Generate a dependency-free SVG showing optimisation progress by function."""

from __future__ import annotations

import html
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from bbo_capstone.data import load_datasets  # noqa: E402


def polyline(points: list[tuple[float, float]]) -> str:
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in points)


def main() -> None:
    datasets = load_datasets()
    width, height = 1440, 820
    panel_width, panel_height = 330, 330
    margin_x, margin_y = 55, 95
    gap_x, gap_y = 25, 45
    colours = ["#0f766e", "#0369a1", "#7c3aed", "#b45309", "#be123c", "#15803d", "#4338ca", "#0e7490"]
    elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#f8fafc"/>',
        '<text x="55" y="48" font-family="Georgia, serif" font-size="28" font-weight="bold" fill="#0f172a">BBO Capstone: Running Best Objective Value</text>',
        '<text x="55" y="72" font-family="Arial, sans-serif" font-size="14" fill="#475569">Each panel is normalised within function because objective scales differ. Higher is better.</text>',
    ]

    for index, dataset in enumerate(datasets):
        row, column = divmod(index, 4)
        left = margin_x + column * (panel_width + gap_x)
        top = margin_y + row * (panel_height + gap_y)
        chart_left, chart_top = left + 42, top + 42
        chart_width, chart_height = panel_width - 60, panel_height - 82
        running_best = np.maximum.accumulate(dataset.y)
        low, high = float(running_best.min()), float(running_best.max())
        scale = high - low if high > low else 1.0
        points = []
        for position, value in enumerate(running_best):
            x = chart_left + chart_width * position / max(len(running_best) - 1, 1)
            y = chart_top + chart_height * (1.0 - (float(value) - low) / scale)
            points.append((x, y))
        colour = colours[index]
        elements.extend(
            [
                f'<rect x="{left}" y="{top}" width="{panel_width}" height="{panel_height}" rx="12" fill="white" stroke="#cbd5e1"/>',
                f'<text x="{left + 18}" y="{top + 27}" font-family="Arial, sans-serif" font-size="17" font-weight="bold" fill="#0f172a">{html.escape(dataset.name)} ({dataset.dimension}D)</text>',
                f'<line x1="{chart_left}" y1="{chart_top + chart_height}" x2="{chart_left + chart_width}" y2="{chart_top + chart_height}" stroke="#94a3b8"/>',
                f'<line x1="{chart_left}" y1="{chart_top}" x2="{chart_left}" y2="{chart_top + chart_height}" stroke="#94a3b8"/>',
                f'<polyline points="{polyline(points)}" fill="none" stroke="{colour}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>',
                f'<circle cx="{points[-1][0]:.1f}" cy="{points[-1][1]:.1f}" r="4.5" fill="{colour}"/>',
                f'<text x="{chart_left}" y="{chart_top + chart_height + 24}" font-family="Arial, sans-serif" font-size="12" fill="#64748b">Round 1</text>',
                f'<text x="{chart_left + chart_width - 42}" y="{chart_top + chart_height + 24}" font-family="Arial, sans-serif" font-size="12" fill="#64748b">Round {len(dataset.y)}</text>',
                f'<text x="{chart_left}" y="{top + panel_height - 13}" font-family="Arial, sans-serif" font-size="12" fill="#475569">Best observed: {dataset.best_value:.6g}</text>',
            ]
        )

    elements.append("</svg>")
    output_path = ROOT / "figures" / "optimisation_history.svg"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(elements), encoding="utf-8")
    print(f"Figure written to: {output_path}")


if __name__ == "__main__":
    main()
