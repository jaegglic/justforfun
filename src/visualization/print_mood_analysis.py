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
from collections import Counter
import re
# Third party requirements
import nltk
from textblob_de import TextBlobDE
# Local imports
from src._paths import PATH_DATA_RAW
from src._settings import PATTERNS_OF_INTEREST
import src.utils as utl

# Constants
_FILENAME = 'MainCompany_2019'


if __name__ == '__main__':

    # Read the pdf
    report = utl.read_pdf(PATH_DATA_RAW, _FILENAME)
    text = report['text']

    # Split into normalized sentences
    sentences = nltk.tokenize.sent_tokenize(text)
    sentences = [utl.normalize_text(sent) for sent in sentences]

    for pat in PATTERNS_OF_INTEREST:
        print(pat)
        polarity = []
        for sent in sentences:
            if re.search(pat, sent) is not None:
                blob = TextBlobDE(sent)
                polarity.append(blob.sentiment.polarity)
        print('    Mean polarity =', sum(polarity)/len(polarity))

