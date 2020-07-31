#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Reads a pdf file and plots the word counts of the most occurring ones.
"""

# -------------------------------------------------------------------------
#   Author(s): Christoph Jaeggli
#   Institute: (none)
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
import src.utils as utl

# Constants
_PDF_FILENAMES = [
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

    'SideCompany_A_2019',

    'SideCompany_B_2019',
]

if __name__ == '__main__':

    # Keywords of interest
    patterns_of_interest = ['mitarbeite', 'kunde']

    # Normalization settings
    stemmer = 'spacy'        # None, 'nltk', 'spacy', or 'personal'

    # How many of the most appearing words to show
    nmost = 10

    # Print space settings
    space_indent = 4
    space_words = 50
    space_count = 15
    space_countword = 15

    # Generate and print the pdf statistics
    for filename in _PDF_FILENAMES:
        # Read the pdf
        report = utl.read_pdf(PATH_DATA_RAW, filename)
        text = report['text']

        # Normalize text
        text = utl.normalize_text(text, stemmer=stemmer)

        # Count the appearances of each (normalized) word
        tokens = text.split()
        counter = Counter(tokens).most_common()

        # Print the Title
        hline = '-' * (space_indent+space_words+space_count+space_countword)
        print('\n' + hline)
        print(f'File {filename}')
        print('')

        # Print the patterns of interest
        for pat in patterns_of_interest:
            sum = 0
            print(f"{' '*space_indent}Pattern r'{pat}'")
            pat = re.compile(pat)
            for i, (word, count) in enumerate(counter):
                if re.match(pat, word) is not None:
                    print(f'{" "*space_indent*2}{i+1:4d} {word} ({count}x)')
                    sum += count
            spw = sum / len(tokens)
            print(f'{" "*space_indent}{"SUM":{space_words}}'
                  f'{sum:<{space_count}}{spw:<{space_countword}.6f}')
            print('')

        # Print the appearances
        print(f'{" "*space_indent}{"WORD":{space_words}}'
              f'{"COUNT":{space_count}}{"COUNT/WORD":<{space_countword}}')
        print(f'{" "*space_indent}{hline[space_indent:]}')
        for word, count in counter[:nmost]:
            cpw = count/len(tokens)
            print(f'{" "*space_indent}{word:{space_words}}'
                  f'{count:<{space_count}}{cpw:<{space_countword}.6f}')
