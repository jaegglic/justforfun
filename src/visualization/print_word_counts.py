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
# Local imports
from src._paths import PATH_DATA_RAW
from src._settings import PATTERNS_OF_INTEREST
import src.utils as utl

# Constants
_FILENAMES = [
    # 'MainCompany_2000',
    # 'MainCompany_2001',
    # 'MainCompany_2002',
    # 'MainCompany_2003',
    # 'MainCompany_2004',
    # 'MainCompany_2005',
    # 'MainCompany_2006',
    # 'MainCompany_2007',
    # 'MainCompany_2008',
    # 'MainCompany_2009',
    # 'MainCompany_2010',
    # 'MainCompany_2011',
    # 'MainCompany_2012',
    # 'MainCompany_2013',
    # 'MainCompany_2014',
    # 'MainCompany_2015',
    # 'MainCompany_2016',
    # 'MainCompany_2017',
    # 'MainCompany_2018',
    'MainCompany_2019',

    # 'SideCompany_A_2019',

    # 'SideCompany_B_2019',

    # 'SideCompany_Y_2019',
]

# Print space settings
_SPACE_INDENT = 4
_SPACE_WORDS = 50
_SPACE_COUNT = 15
_SPACE_COUNTWORD = 15


def _get_word_count_from_pdf(path, filename, stemmer=None):
    """Reads a pdf file and returns a counter for all the appearances of all
    words in the text.

    Args:
        path (Path): Path to the .pdf file.
        filename (str): File name.
        stemmer (str, optional): Stemmer for normalizing the text.

    Returns:
        list of tuple: Return a count in the form (word, count) in descending
            order.
    """
    # Read the pdf
    document = utl.read_pdf(path, filename)
    text = document['text']

    # Normalize text
    text = utl.normalize_text(text, stemmer=stemmer)

    # Count the appearances of each (normalized) word
    tokens = text.split()
    counter = Counter(tokens).most_common()

    return counter


def _print_nmost_appearances(nmost, counter):
    """Prints the `nmost` first words in counter together with the respective
    count in the from
        |    Word    |    Count    |   Count/Word    |
    """

    # Print words and count
    print(f'{" " * _SPACE_INDENT}{"WORD":{_SPACE_WORDS}}'
          f'{"COUNT":{_SPACE_COUNT}}{"COUNT/WORD":<{_SPACE_COUNTWORD}}')
    print(f'{" " * _SPACE_INDENT}{hline[_SPACE_INDENT:]}')
    for word, count in counter[:nmost]:
        cpw = count / len(counter)
        print(f'{" " * _SPACE_INDENT}{word:{_SPACE_WORDS}}'
              f'{count:<{_SPACE_COUNT}}{cpw:<{_SPACE_COUNTWORD}.6f}')


def _print_pattern_of_interest(pat, counter):
    """Print all matches for a given pattern in the form:
        |   Place   |   Word    |    (Count)    |
    where place is the index in `counter`.
    """
    sum = 0
    print(f"{' ' * _SPACE_INDENT}Pattern r'{pat}'")
    for i, (word, count) in enumerate(counter):
        if re.search(pat, word) is not None:
            print(f'{" " * _SPACE_INDENT * 2}{i + 1:4d} {word} ({count}x)')
            sum += count
    spw = sum / len(counter)
    print(f'{" " * _SPACE_INDENT}{"SUM":{_SPACE_WORDS}}'
          f'{sum:<{_SPACE_COUNT}}{spw:<{_SPACE_COUNTWORD}.6f}')


if __name__ == '__main__':

    # Normalization settings
    stemmer = 'spacy'        # None, 'nltk', 'spacy', or 'personal'

    # How many of the most appearing words to show
    nmost = 50

    # Generate and print the pdf statistics
    for filename in _FILENAMES:
        # Get the word count
        counter = _get_word_count_from_pdf(PATH_DATA_RAW, filename, stemmer)

        # Print the Title
        hline = '-' * (_SPACE_INDENT + _SPACE_WORDS + _SPACE_COUNT + _SPACE_COUNTWORD)
        print('\n' + hline)
        print(f'File {filename}')
        print('')

        # Print statistics for all patterns of interest
        for pat in PATTERNS_OF_INTEREST:
            _print_pattern_of_interest(pat, counter)
            print('')

        # Print the appearances
        _print_nmost_appearances(nmost, counter)
