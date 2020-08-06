#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Utilities for the project.
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
from pathlib import Path
import json
# Third party requirements
import PyPDF2
import nltk
from textblob_de import TextBlobDE
import spacy
import pandas as pd
import numpy as np
from sklearn import preprocessing
# Local imports
from src._settings import DF_COL_YEAR, DF_COL_PROFIT, DF_COL_COUNT, DF_COL_POL
from src._settings import PROFIT_NORM


def _german_stop_words():
    """Returns a set of german stop words that are statistically not important
    in the nlp.
    """
    stop_words = nltk.corpus.stopwords.words('german')

    # keep_words = [
    #     'kein', 'keine', 'keinem', 'keinen', 'keiner', 'keines',
    #     'nicht',
    #     'ohne',
    # ]
    keep_words = []

    rem_words = [
        'œ',
        'ˆ',
        'ab',
        'ag',
        'bzw',
        'e',
        'chf', 'mchf', 'tchf',
        'mio',
        'per',
        'seit', 'sowie',
    ]

    stop_words += rem_words
    return [sw for sw in stop_words if sw not in keep_words]


def compute_pat_mood(pattern, sentences):
    """Computes the polarity and the subjectivity of each sentence containing
    the given pattern.

    Args:
        pattern (str): Regex pattern.
        sentences (list of str): List of sentences

    Returns:
        dict: Dict with fields 'sentences', 'polarity' and 'subjectivity' that
            contains the sentence, a polarity, and a subjectivity measure for
            each sentence containing the given pattern.
    """
    pat = re.compile(pattern)
    index, polarity, subjectivity = [], [], []
    for i, sent in enumerate(sentences):
        if re.search(pat, sent) is not None:
            blob = TextBlobDE(sent)
            index.append(i)
            polarity.append(blob.sentiment.polarity)
            subjectivity.append(blob.sentiment.subjectivity)

    mood = dict([
        ('Sentences', [sentences[j] for j in index]),
        ('Polarity', polarity),
        ('Subjectivity', subjectivity)
    ])
    return mood


def get_dataframe_column_names(patterns):
    """Gets the column names for pattern in the dataframe.

    Args:
        patterns (list): List of patterns.

    Returns:
        list: Column names of dataframe.
    """
    columns = []
    for ipat in range(len(patterns)):
        columns.append(f'{DF_COL_COUNT}{ipat:02.0f}')
        columns.append(f'{DF_COL_POL}{ipat:02.0f}')
    return columns


def get_sentences_from_pdf(path, filename):
    """Reads a pdf file and returns the list of sentences.

    Args:
        path (Path): Path to the .pdf file.
        filename (str): File name.

    Returns:
        list of str: List of sentences.
    """
    # Read the PDF
    report = read_pdf(path, filename)
    text = report['text']

    # Split into Normalized Sentences
    sentences = nltk.tokenize.sent_tokenize(text)
    sentences = [normalize_text(sent) for sent in sentences]

    return sentences


def get_shifted_columns(df, nmax):
    """Shifts all the columns up to nmax locations.

    Notes:
        If `nmax` is 2 and the data frame is given by

                col_a   col_b
            0     10     2.0
            1     11     2.1
            2     12     2.2
            3     13     2.3

        then the resulting data frame is given by

                col_a   col_b  col_a-1 col_b-1 col_a-2 col_b-2
            0     10     2.0     NaN     NaN     NaN     NaN
            1     11     2.1     10      2.0     NaN     NaN
            2     12     2.2     11      2.1     10      2.0
            3     13     2.3     12      2.2     11      2.1

    Args:
        df (DataFrame): Data
        nshift (int): Maximal number of shifts.

    Returns:
        DataFrame: Data with the shifted columns
    """
    columns = df.columns
    for i in range(nmax):
        k = i+1
        for col in columns:
            col_new = f'{col}-{k}'
            shifted = pd.DataFrame(
                data=np.array(df[col].iloc[:-k]),
                index=df.index[k:],
                columns=[col_new],
            )
            df = pd.concat([df, shifted], axis=1, ignore_index=False)

    return df


def load_data(files, patterns, normalized=False):
    """Reads a set of .json files and generates a time series.

    The output DataFrame has the columns as defined in the `_settings.py` file
    (DF_COL_*), for example:
        - 'Year':           Year of the data row
        - 'Profit':         Time series of profit
        - 'Count_00':       Time series of count for pattern 0
        - 'Polarity_00':    Time series of polarity for pattern 0
        - ...
        - 'Count_n':        Time series of count for pattern n
        - 'Polarity_n':     Time series of polarity for pattern n

        Args:
            files (iterator of Path objects): .json file names.
            patterns (list of str): Patterns to consider.
            normalized (bool): Normalize data sets for columns `pat_i`

        Returns:
            DataFrame: Time series.
        """
    data = []
    columns = [DF_COL_YEAR, DF_COL_PROFIT]
    columns.extend(get_dataframe_column_names(patterns))

    for file in files:
        # Load content of data file
        with open(str(file), 'r') as jfile:
            content = json.load(jfile)

        # Read year and profit
        year = int(content['Metadata']['Year'])
        profit = content['Data']['Profit'] / PROFIT_NORM
        new_row = [year, profit]

        # Compute polarities for all patterns
        for pat in patterns:
            mood = content['Data']['Mood'][pat]
            new_row.append(len(mood['Sentences']))

            mean_polarity = sum(mood['Polarity']) / len(mood['Polarity'])
            new_row.append(mean_polarity)

        # Append new row
        data.append(new_row)
    data = np.array(data)

    if normalized:
        data[:, 2:] = preprocessing.normalize(data[:, 2:], norm='l1', axis=0)

    return pd.DataFrame(data=data, columns=columns)


def normalize_text(text, stemmer=None):
    """Minor normalization of a string by using techniques:
        - all lower case
        - alphanumeric (no numbers etc.)
        - remove stop words
        - (evtl.) stemmer

    Args:
        text (str): Text to be normalized
        stemmer (str {None, 'nltk', 'spacy'}, optional): Usage of no, 'nltk',
            or 'spacy' stemmer.

    Returns:
        str: Normalized string.
    """

    pat = r'\n'
    repl = r' '
    re.sub(pat, repl, text)

    # Build word-tokens
    words = nltk.tokenize.word_tokenize(text)

    # Lower case all words
    words = [t.lower() for t in words]
    words = [t for t in words if t.isalpha()]

    # Remove stop words
    stop_words = _german_stop_words()
    words = [t for t in words if t not in stop_words]

    # Stemming the words
    if stemmer == 'nltk':
        german = nltk.snowball.GermanStemmer()
        words = [german.stem(w) for w in words]
    elif stemmer == 'spacy':
        nlp = spacy.load('de_core_news_sm')
        words = [nlp.tokenizer(w)[0].lemma_ for w in words]

    return ' '.join(words)


def read_pdf(path, filename):
    """Reads a pdf file.

    Notes
        The pages can be regained by::

            pat = document['metadata']['page_sep']
            text = document['text']
            pages = re.split(pat, text)

    Args:
        path (Path): Path to the .pdf file.
        filename (str): File name.

    Returns:
        dict: PDF text plus additional information.
    """

    file = Path(path, filename).with_suffix('.pdf')
    with open(file, 'rb') as pfile:
        # Generate pdf reader object
        reader = PyPDF2.PdfFileReader(pfile)
        npages = reader.numPages

        # Concatenate text
        text = ''
        for num in range(npages):
            page = reader.getPage(num)
            text += f'<PageNum{num+1:03}>{page.extractText()}'

    # Generate report object with metadata
    document = {
        'metadata': {
            'type':         'PDF',
            'name':         str(file),
            'npages':       npages,
            'page_sep':     r'<PageNum[0-9]{3}>'
        },
        'text':     text,
    }

    return dict(document)
