#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Reads a pdf file and plots the word counts of the most occurring ones.
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
# Third party requirements
# Local imports
from src._paths import PATH_DATA_RAW
from src._settings import PATTERNS_OF_INTEREST
import src.utils as utl

# Constants
_FILENAME = 'MainCompany_2019'

# _FILENAME = 'SideCompany_A_2019'
# _FILENAME = 'SideCompany_B_2019'
# _FILENAME = 'SideCompany_Y_2019'


def _print_pol_and_subj(pat, sentences, indent=4, dec=3):
    """Prints the mean polarity and mean subjectivity of a pattern per
    sentence.
    """
    # Compute polarity and subjectivity
    mood = utl.compute_pat_mood(pat, sentences)

    # Print statistics for the given pattern
    print(f'{" " * indent}{pat}')
    pol = sum(mood['Polarity']) / len(mood['Polarity'])
    subj = sum(mood['Subjectivity']) / len(mood['Subjectivity'])
    print(f'{" "*indent*2}Polarity     = {pol:{dec+2}.{dec}f}')
    print(f'{" "*indent*2}Subjectivity = {subj:{dec+2}.{dec}f}')


if __name__ == '__main__':

    # Get sentences from the file
    sentences = utl.get_sentences_from_pdf(PATH_DATA_RAW, _FILENAME)

    # Print the Title
    print('')
    print(f'File {_FILENAME}')
    print('')

    # Print Mean Polarity and Subjectivity
    for pat in PATTERNS_OF_INTEREST:
        _print_pol_and_subj(pat, sentences)

