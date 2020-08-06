#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Models the profit by considering the past time series.
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
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.neural_network import MLPRegressor
# Local imports
from src._paths import PATH_DATA_PROCESSED
from src._settings import PATTERNS_OF_INTEREST, SEED
import src.utils as utl

# Constants
_NPAST = 3
_NKFOLD = 5


def predict_next_years_profit(df, clf, npast):
    """Predicts the profit of next year based on the reports of this year.

    Args:
        df (DataFrame): DataFrame (c.f. `utl.load_data`)
        clf (sklearn.Classifier): Classifier for the prediction
        nshiftmax (int): Number of past years to consider

    Returns:
        int: Profit of next year.
    """

    # Generate shifted parameters
    nmax = npast-1         # the removed "1" shift is added in X_train and y_train
    columns = utl.get_dataframe_column_names(PATTERNS_OF_INTEREST)
    X = df[columns]
    X = utl.get_shifted_columns(X, nmax).values
    y = df['Profit'].values

    # Reduce to non-NaN values (and shift the values one instance)
    X_train = X[nmax:-1, :]
    X_pred = X[-1, :].reshape(1, -1)
    y_train = y[nmax+1:]

    # # Train and Predict
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_pred)

    return y_pred[0]


if __name__ == '__main__':

    # Load data
    files = Path(PATH_DATA_PROCESSED).glob("*.json")
    df = utl.load_data(files, PATTERNS_OF_INTEREST, normalized=True)

    # Get prediction for next year
    # clf = KNeighborsRegressor(random_state=SEED)
    clf = DecisionTreeRegressor(random_state=SEED)
    # clf = MLPRegressor(random_state=SEED, max_iter=10000, hidden_layer_sizes=(20, 20))
    profit = predict_next_years_profit(df, clf, _NPAST)

    print('')
    print(f'Beliefing the classifier "{clf.__class__.__name__}"\n'
          f'the profit will be {profit:.1f} MSFr.')



