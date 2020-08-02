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
import json
# Third party requirements
import matplotlib.pyplot as plt
import numpy as np
# Local imports
from src._paths import PATH_DATA_PROCESSED
from src._settings import PATTERNS_OF_INTEREST


if __name__ == '__main__':

    # Define pattern
    pat = PATTERNS_OF_INTEREST[0]

    # Load data sets
    xticklabel = []
    polarity, subjectivity, profit = [], [], []
    data_files = Path(PATH_DATA_PROCESSED).glob("*.json")
    for dfile in data_files:
        print(f'Loading {dfile.parts[-1]}...', end='')
        with open(str(dfile), 'r') as jfile:
            data = json.load(jfile)
        mood = data['Data']['Mood'][pat]

        # Get polarity, subjectivity, and profit data
        polarity.append(sum(mood['polarity'])/len(mood['polarity']))
        subjectivity.append(sum(mood['subjectivity'])/len(mood['subjectivity']))
        profit.append(data['Data']['Profit'])

        # Get year xticklabel
        xticklabel.append(dfile.parts[-1].split('.')[0].split('_')[-1])

        print('done')

    # Print figures
    xticks = np.arange(len(xticklabel))
    _, ax = plt.subplots(3, 1)

    ax[0].plot(xticks, np.array(polarity))
    ax[0].set_xticks(xticks)
    ax[0].set_xticklabels(xticklabel)
    ax[0].set_ylim((-1, 1))

    ax[1].plot(xticks, np.array(subjectivity))
    ax[1].set_xticks(xticks)
    ax[1].set_xticklabels(xticklabel)
    ax[1].set_ylim((0, 1))

    ax[2].plot(xticks, np.array(profit))
    ax[2].set_xticks(xticks)
    ax[2].set_xticklabels(xticklabel)

    plt.show()