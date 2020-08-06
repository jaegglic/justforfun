#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Makes the data sets by reading pdf files and adding some information.

The data sets are json files of the form:
    {
      "Metadata": {
        "filename": str
      },
      "Data": {
        "Premium":   int,
        "Profit":    int,
        "Equity":    int,
        "Mood": {
          "pat_01":     dict (as in `utl.compute_pat_mood`)
          "pat_02":     dict ( " )
          ....
      }
    }
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
# Local imports
from src._paths import PATH_DATA_RAW, PATH_DATA_PROCESSED
from src._settings import PATTERNS_OF_INTEREST
import src.utils as utl

# Constants

if __name__ == '__main__':
    pdf_files = Path(PATH_DATA_RAW).glob("*.pdf")
    json_files = Path(PATH_DATA_RAW).glob("*.json")

    for pdf_file, json_file in zip(pdf_files, json_files):

        # Check if they are referring to the corresponding file
        filename = pdf_file.parts[-1].split('.')[0]
        if filename != json_file.parts[-1].split('.')[0]:
            raise ValueError(f'{pdf_file.parts[-1]} and {json_file.parts[-1]} '
                             f'do not refer to corresponding files.')
        print(f'Generate data set {filename}...', end='')

        # Get a list of sentences from the pdf
        sentences = utl.get_sentences_from_pdf(PATH_DATA_RAW, filename)

        # Get additional data from .json file
        with open(str(json_file), 'r') as jfile:
            data = json.load(jfile)

        # Compute polarity and subjectivities for each pattern
        data['Data']['Mood'] = {}
        for pat in PATTERNS_OF_INTEREST:
            mood = utl.compute_pat_mood(pat, sentences)
            data['Data']['Mood'][str(pat)] = mood

        # Save data set
        file = Path(PATH_DATA_PROCESSED, filename).with_suffix('.json')
        with open(file, 'w') as dfile:
            json.dump(data, dfile)
        print('done')

