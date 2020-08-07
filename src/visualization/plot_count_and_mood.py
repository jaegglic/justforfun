#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Plots the polarity and the subjectivity.
"""

# -------------------------------------------------------------------------
#   Author(s): Christoph Jaeggli
#   Institute: (None)
#
#   MIT License
#   Copyright (c) 2020 Christoph Jaeggli
#
#   This program is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

# Standard library
from pathlib import Path
# Third party requirements
import matplotlib.pyplot as plt
import numpy as np
# Local imports
from src._paths import PATH_DATA_PROCESSED
from src._settings import PATTERNS_OF_INTEREST, DF_COL_COUNT, DF_COL_POL
from src._settings import CLR_CHART_12
import src.utils as utl


# Constants
_LINEWIDTH = 2
_MARKERSIZE = 12


if __name__ == '__main__':

    # Load data sets
    files = Path(PATH_DATA_PROCESSED).glob("*.json")
    df = utl.load_data(files, PATTERNS_OF_INTEREST, normalized=False)

    # Get year xticks
    xticklabel = [f'{y:4.0f}' for y in df['Year']]
    xticks = np.arange(len(xticklabel))

    # Print
    rotation = 90
    for ipat, pat in enumerate(PATTERNS_OF_INTEREST):
        # Plot Counts
        col = f'{DF_COL_COUNT}{ipat:02.0f}'
        _, ax = plt.subplots(1, 1, figsize=(7, 4))
        ax.plot(xticks, df[col], color=CLR_CHART_12, linewidth=_LINEWIDTH)
        ax.plot(xticks, df[col], color=CLR_CHART_12, marker='o', markersize=_MARKERSIZE)
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticklabel, rotation=rotation)
        ax.set_title(f'Count of {pat}')

        # Plot Polarity
        col = f'{DF_COL_POL}{ipat:02.0f}'
        _, ax = plt.subplots(1, 1, figsize=(7, 4))
        ax.plot(xticks, df[col], color=CLR_CHART_12, linewidth=_LINEWIDTH)
        ax.plot(xticks, df[col], color=CLR_CHART_12, marker='o', markersize=_MARKERSIZE)
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticklabel, rotation=rotation)
        ax.set_title(f'Polarity of {pat}')

    # Plot Profit
    col = 'Profit'
    _, ax = plt.subplots(1, 1, figsize=(7, 4))
    ax.plot(xticks, df[col], color=CLR_CHART_12, linewidth=_LINEWIDTH)
    ax.plot(xticks, df[col], color=CLR_CHART_12, marker='o', markersize=_MARKERSIZE)
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabel, rotation=rotation)
    ax.set_title(col)

    plt.show()
