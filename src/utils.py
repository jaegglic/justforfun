#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Utilities for the project.
"""

# -------------------------------------------------------------------------
#   Author(s): Christoph Jaeggli
#   Institute: Insel Data Science Center, Insel Gruppe AG
#
#   MIT License
#   Copyright (c) 2020 Insel Data Science Center
#
#   This program is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

# Standard library
import re
from pathlib import Path
from collections import Counter
# Third party requirements
import PyPDF2
import nltk
import spacy
# Local imports
from src._paths import PATH_DATA_RAW
from src.features._lemmatizer import GermanLemmatizer


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


def normalize_text(text, stemmer=None):
    """Minor normalization of a string by using techniques:
        - all lower case
        - alphanumeric (no numbers etc.)
        - remove stop words
        - (evtl.) stemmer

    Args:
        text (str): Text to be normalized
        stemmer (str {None, 'nltk', 'spacy', 'personal'}, optional): Usage of
            no, 'nltk', 'spacy', or 'personal' stemmer.

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
    elif stemmer == 'personal':
        german = GermanLemmatizer()
        words = [german.lemma(w) for w in words]

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
            text += f'<PageNum{num:03}>{page.extractText()}'

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
