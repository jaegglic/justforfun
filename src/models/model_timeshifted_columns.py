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
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVC, LinearSVC
from sklearn.tree import DecisionTreeRegressor
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression, SGDClassifier, Perceptron
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report
# Local imports
from src._paths import PATH_DATA_PROCESSED
from src._settings import PATTERNS_OF_INTEREST
import src.utils as utl

# Constants
_NPAST = 3
_NKFOLD = 5

# Classifiers to be tested and compared
# CLF = KNeighborsRegressor()
# CLF = SVC()
# CLF = LinearSVC()
CLF = DecisionTreeRegressor()
# CLF = MultinomialNB()
# CLF = LogisticRegression()
# CLF = SGDClassifier()
# CLF = Perceptron()
# CLF = MLPClassifier()


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
    X = df[PATTERNS_OF_INTEREST]
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

    # Get prediction for next year
    files = Path(PATH_DATA_PROCESSED).glob("*.json")
    df = utl.load_data(files, PATTERNS_OF_INTEREST, normalized=True)
    profit = predict_next_years_profit(df, CLF, _NPAST)

    print('')
    print(f'Beliefing the classifier "{CLF.__class__.__name__}"\n'
          f'the profit will be {profit:.0f} SFr.')



