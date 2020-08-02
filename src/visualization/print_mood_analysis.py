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
import re
# Third party requirements
import nltk
from textblob_de import TextBlobDE
# Local imports
from src._paths import PATH_DATA_RAW
from src._settings import PATTERNS_OF_INTEREST
import src.utils as utl

# Constants
# _FILENAME = 'MainCompany_2019'
_FILENAME = 'SideCompany_A_2019'


def _get_sentences_from_pdf(path, filename):
    """Reads a pdf file and returns the list of sentences.

    Args:
        path (Path): Path to the .pdf file.
        filename (str): File name.

    Returns:
        list of str: List of sentences.
    """
    # Read the PDF
    report = utl.read_pdf(path, filename)
    text = report['text']

    # Split into Normalized Sentences
    sentences = nltk.tokenize.sent_tokenize(text)
    sentences = [utl.normalize_text(sent) for sent in sentences]

    return sentences


def _print_pol_and_subj(pat, sentences, indent=4, dec=3):
    """Prints the mean polarity and mean subjectivity of a pattern per
    sentence.
    """
    print(f'{" "*indent}{pat}')
    polarity = []
    subjectivity = []
    for sent in sentences:
        if re.search(pat, sent) is not None:
            blob = TextBlobDE(sent)
            polarity.append(blob.sentiment.polarity)
            subjectivity.append(blob.sentiment.subjectivity)

    pol = sum(polarity) / len(polarity)
    subj = sum(subjectivity) / len(subjectivity)
    print(f'{" "*indent*2}Polarity     = {pol:{dec+2}.{dec}f}')
    print(f'{" "*indent*2}Subjectivity = {subj:{dec+2}.{dec}f}')


if __name__ == '__main__':

    # Get sentences from the file
    sentences = _get_sentences_from_pdf(PATH_DATA_RAW, _FILENAME)

    # Print the Title
    print('')
    print(f'File {_FILENAME}')
    print('')

    # Print Mean Polarity and Subjectivity
    for pat in PATTERNS_OF_INTEREST:
        _print_pol_and_subj(pat, sentences)

