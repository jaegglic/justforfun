#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generates and plots the prediction of next years profit.
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
from sklearn.linear_model import SGDRegressor
from sklearn.ensemble import BaggingRegressor, RandomForestRegressor
# Local imports
from src._paths import PATH_DATA_PROCESSED, PATH_REP_FIG
from src._settings import PATTERNS_OF_INTEREST, SEED, PROFIT_UNIT
from src._settings import CLR_CHART_02, CLR_CHART_12, FONTSIZE,\
    MARKERSIZE, LINEWIDTH
import src.utils as utl
from src.visualization.print_clf_performance import predict_next_years_profit

# Constants
_NPAST = 3

if __name__ == '__main__':

    # Fix random state
    np.random.seed(SEED)

    # Load data
    files = Path(PATH_DATA_PROCESSED).glob("*.json")
    df = utl.load_data(files, PATTERNS_OF_INTEREST, normalized=True)

    # Predict new value
    clf = BaggingRegressor()
    profit_new = predict_next_years_profit(df, clf, _NPAST)
    print('')
    print(f'Beliefing the classifier "{clf.__class__.__name__}"\n'
          f'the profit will be {profit_new:.1f} [{PROFIT_UNIT}]')

    # Get year xticks
    xticklabel = [f'{y:4.0f}' for y in df['Year']]
    xticklabel.append(f'{int(xticklabel[-1])+1:4.0f}')
    xticks = np.arange(len(xticklabel))

    # Plot figure
    rotation = 90
    profit_old = [p for p in df['Profit']]
    plt.rcParams.update({'font.size': FONTSIZE})
    _, ax = plt.subplots(1, 1, figsize=(7, 4))

    ax.plot(xticks[-2:], [profit_old[-1], profit_new],
            color=CLR_CHART_02, linewidth=LINEWIDTH)
    ax.plot(xticks[-1], profit_new, color=CLR_CHART_02,
            marker='o', markersize=MARKERSIZE, markeredgecolor='#ffffff')

    ax.plot(xticks[:-1], profit_old, color=CLR_CHART_12, linewidth=LINEWIDTH)
    ax.plot(xticks[:-1], profit_old, color=CLR_CHART_12,
            marker='o', markersize=MARKERSIZE, markeredgecolor='#ffffff')

    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabel, rotation=90)

    plt.tight_layout()
    utl.save_fig(PATH_REP_FIG, 'Prediction', plt)
    plt.show()
