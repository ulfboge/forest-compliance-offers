"""Generate placeholder visuals for the EUDR traceability demo.

The figures are intentionally lightweight so the script can run without
GeoPandas or other heavy geospatial dependencies. Each graphic saves into
`docs/Visuals/` and overwrites existing files so the repository can be
refreshed quickly during workshops.
"""

from __future__ import annotations

import random
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


BASE_DIR = Path(__file__).resolve().parents[1]
VISUALS_DIR = BASE_DIR / "docs" / "Visuals"


def _reset_matplotlib() -> None:
    plt.close("all")
    plt.rcParams.update(
        {
            "figure.figsize": (8, 6),
            "axes.titlesize": 14,
            "axes.labelsize": 11,
            "font.family": "DejaVu Sans",
            "axes.facecolor": "#f6f7f9",
            "axes.edgecolor": "#d0d3d8",
            "axes.grid": True,
            "grid.color": "#dfe3e8",
        }
    )


def _ensure_output_dir() -> None:
    VISUALS_DIR.mkdir(parents=True, exist_ok=True)


def _plot_overview_map(seed: int = 42) -> None:
    rng = random.Random(seed)
    fig, ax = plt.subplots()

    risk_colors = {"Low": "#2e8b57", "Medium": "#f0a202", "High": "#d62828"}
    legend_handles = []

    for idx, risk in enumerate(["Low", "Low", "Medium", "High", "Low"], start=1):
        center_x = rng.uniform(0.1, 0.9)
        center_y = rng.uniform(0.1, 0.9)
        width = rng.uniform(0.12, 0.18)
        height = rng.uniform(0.12, 0.18)

        rect = plt.Rectangle(
            (center_x - width / 2, center_y - height / 2),
            width,
            height,
            facecolor=risk_colors[risk],
            alpha=0.6,
            edgecolor="black",
            linewidth=1.2,
        )
        ax.add_patch(rect)
        ax.text(
            center_x,
            center_y,
            f"ANG-00{idx}\n{risk}",
            ha="center",
            va="center",
            fontsize=10,
            color="white" if risk != "Low" else "#0f2f1e",
            weight="bold",
        )

        if risk not in [handle.get_label() for handle in legend_handles]:
            legend_handles.append(
                plt.Rectangle((0, 0), 1, 1, facecolor=risk_colors[risk], label=risk)
            )

    ax.set_title("Supplier Group Overview – EUDR Risk Classes")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.legend(handles=legend_handles, frameon=False, loc="upper right", title="Risk Level")
    ax.set_aspect("equal")

    fig.tight_layout()
    fig.savefig(VISUALS_DIR / "eudr_risk_map_overview.png", dpi=200)


def _plot_risk_classification(seed: int = 99) -> None:
    rng = np.random.default_rng(seed)
    fig, ax = plt.subplots()

    suppliers = ["ANG-001", "ANG-002", "ANG-003", "ANG-004", "ANG-005"]
    risk_score = np.array([0.2, 0.25, 0.55, 0.85, 0.35])
    disturbance = rng.normal(loc=[5, 7, 14, 22, 9], scale=2.5)

    color_map = np.array(["#2e8b57", "#2e8b57", "#f0a202", "#d62828", "#2e8b57"])

    ax.scatter(
        disturbance,
        risk_score * 100,
        s=220,
        c=color_map,
        edgecolor="black",
        linewidth=1,
    )

    for sup, x, y in zip(suppliers, disturbance, risk_score):
        ax.text(x, y * 100 + 2.5, sup, ha="center", va="bottom", fontsize=10)

    ax.set_title("Spatial Risk Classification (Demo)")
    ax.set_xlabel("Radar Disturbance Alerts (count)")
    ax.set_ylabel("Composite Risk Score (%)")
    ax.set_ylim(0, 100)
    ax.grid(True, linestyle="--", alpha=0.5)

    fig.tight_layout()
    fig.savefig(VISUALS_DIR / "eudr_risk_classification_map.png", dpi=200)


def _plot_forest_loss_bar() -> None:
    fig, ax = plt.subplots()

    periods = ["2020", "2021", "2022", "2023", "2024"]
    loss_values = [0, 25, 65, 110, 50]

    bars = ax.bar(periods, loss_values, color="#457b9d", edgecolor="#1d3557")
    ax.set_title("Forest Loss Detected (ha)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Hectares")
    ax.bar_label(bars, padding=4)

    fig.tight_layout()
    fig.savefig(VISUALS_DIR / "eudr_forest_loss_bar.png", dpi=200)


def main() -> None:
    _reset_matplotlib()
    _ensure_output_dir()
    _plot_overview_map()
    _plot_risk_classification()
    _plot_forest_loss_bar()
    print(f"Generated visuals in {VISUALS_DIR}")


if __name__ == "__main__":
    main()
 