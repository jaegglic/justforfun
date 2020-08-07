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
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.linear_model import TweedieRegressor, SGDRegressor
from sklearn.svm import LinearSVR, SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import BaggingRegressor, RandomForestRegressor
from sklearn.neural_network import MLPRegressor
# Local imports
from src._paths import PATH_DATA_PROCESSED
from src._settings import PATTERNS_OF_INTEREST, SEED, PROFIT_UNIT
import src.utils as utl

# Constants
_NPAST = 3
_NKFOLD = 5
_CLF = [
    LinearRegression(),
    Ridge(),
    Lasso(),
    TweedieRegressor(),
    SGDRegressor(max_iter=1000000),
    LinearSVR(),
    SVR(),
    KNeighborsRegressor(),
    DecisionTreeRegressor(),
    BaggingRegressor(),
    RandomForestRegressor(),
    # MLPRegressor(max_iter=1000000),
]


def _get_supervised_set(df, npast):
    """Returns the part of the data for which the answer is known."""
    # Generate shifted parameters
    nmax = npast-1         # the removed "1" shift is treated below
    columns = utl.get_dataframe_column_names(PATTERNS_OF_INTEREST)
    X = df[columns]
    X = utl.get_shifted_columns(X, nmax).values
    y = df['Profit'].values

    # Reduce to non-NaN values and shift the values one instance
    X = X[nmax:-1, :]
    y = y[nmax+1:]

    return X, y


def _get_unsupervised_set(df, npast):
    """Returns the part of the data for which the answer is unknown."""
    # Generate shifted parameters
    nmax = npast-1         # the removed "1" shift is treated below
    columns = utl.get_dataframe_column_names(PATTERNS_OF_INTEREST)
    X = df[columns]
    X = utl.get_shifted_columns(X, nmax).values

    # Return last instance for which the answer is not known
    return X[-1, :].reshape(1, -1)


def predict_next_years_profit(df, clf, npast):
    """Predicts the profit of next year based on the reports of this year.

    Args:
        df (DataFrame): DataFrame (c.f. `utl.load_data`)
        clf (sklearn.Classifier): Classifier for the prediction
        npast (int): Number of past years to consider

    Returns:
        int: Profit of next year.
    """

    # Get datasets
    X_train, y_train = _get_supervised_set(df, npast)
    X_pred = _get_unsupervised_set(df, npast)

    # Train and Predict
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_pred)

    return y_pred[0]


def measure_clf_score(df, clf, npast, nkfold=10):
    """Measures the accuracy of a classifier by cross validation.

    Args:
        df (DataFrame): DataFrame (c.f. `utl.load_data`)
        clf (sklearn.Classifier): Classifier for the prediction
        npast (int): Number of past years to consider
        nkfold (int): Number of folds for cross validation.

    Returns:
        float: Profit of next year.
    """
    # Define KFold cross-validator
    kfold = KFold(n_splits=nkfold)

    # Get data
    X, y = _get_supervised_set(df, npast)

    # Iteratively fit and test all k folds
    y_test_all = []
    y_pred_all = []
    for k, (ind_train, ind_test) in enumerate(kfold.split(X)):

        # Split the test/train set according to the fold indices
        X_train, X_test = X[ind_train], X[ind_test]
        y_train, y_test = y[ind_train], y[ind_test]

        # Train and Predict
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)

        # Assemble test and pred results
        y_test_all.extend(y_test)
        y_pred_all.extend(y_pred)

    # Compute accuracies
    rmse = np.sqrt(mean_squared_error(y_test_all, y_pred_all))
    r2 = r2_score(y_test_all, y_pred_all)

    return rmse, r2


if __name__ == '__main__':
    space_indent = 4
    space_clf = 30
    space_profit = 6

    # Load data
    files = Path(PATH_DATA_PROCESSED).glob("*.json")
    df = utl.load_data(files, PATTERNS_OF_INTEREST, normalized=True)

    # Get prediction for next year for each classifier
    results = []
    for clf in _CLF:
        # Fix random state
        np.random.seed(SEED)

        # Compute cross validation performance
        name = clf.__class__.__name__
        print(f'{name}...', end='')
        profit = predict_next_years_profit(df, clf, _NPAST)
        rmse, r2 = measure_clf_score(df, clf, _NPAST, _NKFOLD)
        res = (
            clf.__class__.__name__,
            profit,
            rmse,
            r2,
        )
        results.append(res)
        print('done')

    # Order performances
    # Use sort_index =
    #   - 0 and `reverse=False`  for alphabetical names
    #   - 1 and `reverse=True`  for highest profit first
    #   - 2 and `reverse=False` for lowest RMSE first
    #   - 3 and `reverse=True` for highest  R2 score first
    sort_index = 2
    reverse = False
    results.sort(key=lambda x: x[sort_index], reverse=reverse)

    # Print performances
    print(f'\nNext years profit prediction in [{PROFIT_UNIT}] is:')
    for nm, profit, rmse, r2 in results:
        print(f'{" "*space_indent}', end='')
        print(f'{nm:{space_clf}}', end='')
        print(f'{profit:{space_profit}.1f}', end='')
        print(f'{" "*space_indent}(RMSE = {rmse:6.1f}, R2 = {r2:6.3f})')



