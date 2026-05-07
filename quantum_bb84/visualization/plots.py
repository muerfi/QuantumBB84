"""Optional plotting helpers for simulation summaries."""

from __future__ import annotations

from pathlib import Path
from typing import Sequence


def save_qber_plot(noise_levels: Sequence[float], qber_values: Sequence[float], output_path: str | Path) -> Path:
    """Save a simple QBER-vs-noise plot using robust path handling.

    Matplotlib is imported lazily so the core simulation package remains usable
    in environments without plotting dependencies.
    """

    import matplotlib.pyplot as plt

    path = Path(output_path).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots()
    ax.plot(noise_levels, qber_values, marker="o")
    ax.set_xlabel("Noise probability")
    ax.set_ylabel("Observed QBER")
    ax.set_title("Finite-shot QBER under toy noise")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    return path
