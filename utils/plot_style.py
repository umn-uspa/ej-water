"""Shared Matplotlib plotting style for all plotting notebooks."""

from __future__ import annotations

import matplotlib as mpl
import textwrap


STYLE_PARAMS = {
    "font.sans-serif": ["Nimbus Roman"],
    "font.family": "sans-serif",
    "font.size": 8,
    "axes.labelsize": 10,
    "axes.titlesize": 10,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "legend.title_fontsize": 10,
}


def apply_plot_style() -> None:
    """Apply project-wide plotting defaults."""
    mpl.rcParams.update(STYLE_PARAMS)


def wrap_labels(ax, width, axis="x", break_long_words=False):
    """Wrap x- or y-axis tick labels to a fixed character width."""
    labels = []
    ticklabels = ax.get_xticklabels() if axis == "x" else ax.get_yticklabels()
    for label in ticklabels:
        text = label.get_text()
        labels.append(
            textwrap.fill(text, width=width, break_long_words=break_long_words)
        )
    if axis == "x":
        ax.set_xticklabels(labels, rotation=0)
    else:
        ax.set_yticklabels(labels, rotation=0)
