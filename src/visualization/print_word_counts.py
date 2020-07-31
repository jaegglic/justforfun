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
# Third party requirements
# Local imports
from src._paths import PATH_DATA_RAW
import src.utils as utl

# Constants
_PDF_FILENAMES = [
    # 'Mobiliar_GB_2010',
    # 'Mobiliar_GB_2011',
    # 'Mobiliar_GB_2012',
    # 'Mobiliar_GB_2013',
    # 'Mobiliar_GB_2014',
    # 'Mobiliar_GB_2015',
    # 'Mobiliar_GB_2016',
    # 'Mobiliar_GB_2017',
    # 'Mobiliar_GB_2018',
    'Mobiliar_GB_2019',

    # 'InselGruppe_KR_2019',
]

if __name__ == '__main__':
    nmost = 20

    reports = []
    for filename in _PDF_FILENAMES:
        # Read the pdf
        report = utl.read_pdf(PATH_DATA_RAW, filename)

        text = report['text']
        tokens = text.split()

        # Counter
        nword = 50
        ncount = 15
        ncountword = 15
        counter = Counter(tokens).most_common()
        print(f'\nReport {filename}')
        print(f'    {"Word":{nword}}{"Count":{ncount}}{"Count/Word":<{ncountword}}')
        for word, count in counter[:nmost]:
            cpw = count/len(tokens)
            print(f'    {word:{nword}} {count:<{ncount}} {cpw:>{ncountword}.6f}')





