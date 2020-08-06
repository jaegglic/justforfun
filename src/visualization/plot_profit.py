#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Plots the prediction of next years profit.
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
from sklearn.svm import SVC, LinearSVC
from sklearn.linear_model import LogisticRegression
# Local imports
from src._paths import PATH_DATA_PROCESSED
from src._settings import PATTERNS_OF_INTEREST
from src._settings import CLR_CHART_02, CLR_CHART_12
import src.utils as utl
from src.models.model_timeshifted_columns import predict_next_years_profit


# Constants
_NPAST = 2
_LINEWIDTH = 4
_MARKERSIZE = 12


if __name__ == '__main__':

    # Load data sets
    files = Path(PATH_DATA_PROCESSED).glob("*.json")
    df = utl.load_data(files, PATTERNS_OF_INTEREST, normalized=True)

    # Predict new value
    clf = SVC()
    profit_new = predict_next_years_profit(df, clf, _NPAST)

    # Get year xticks
    xticklabel = [f'{y:4.0f}' for y in df['Year']]
    xticklabel.append(f'{int(xticklabel[-1])+1:4.0f}')
    xticks = np.arange(len(xticklabel))

    # Plot figure
    profit_old = [p for p in df['Profit']]
    _, ax = plt.subplots(1, 1, figsize=(7, 4))

    ax.plot(xticks[-2:], [profit_old[-1], profit_new], color=CLR_CHART_02, linewidth=_LINEWIDTH, linestyle='--')
    ax.plot(xticks[-1], profit_new, color=CLR_CHART_02, marker='o', markersize=_MARKERSIZE)

    ax.plot(xticks[:-1], profit_old, color=CLR_CHART_12, linewidth=_LINEWIDTH)
    ax.plot(xticks[:-1], profit_old, color=CLR_CHART_12, marker='o', markersize=_MARKERSIZE)

    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabel)


    plt.show()
