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
# Third party requirements
import PyPDF2
import nltk
from textblob_de import TextBlobDE
import spacy
# Local imports


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
        dictz: Dict with fields 'sentences', 'polarity' and 'semtiment' that
            contains the sentence, a polarity, and a subjectivity measure for
            each sentence containing the given pattern.
    """
    pat = re.compile(pattern)
    index, polarity, subjectivity =[], [], []
    for i, sent in enumerate(sentences):
        if re.search(pat, sent) is not None:
            blob = TextBlobDE(sent)
            index.append(i)
            polarity.append(blob.sentiment.polarity)
            subjectivity.append(blob.sentiment.subjectivity)

    mood = dict([
        ('sentences', [sentences[j] for j in index]),
        ('polarity', polarity),
        ('subjectivity', subjectivity)
    ])
    return mood


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
