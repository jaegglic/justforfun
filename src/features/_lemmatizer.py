#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Defines a personalized stemmer adapted to the data (not complete at all).
"""

# -------------------------------------------------------------------------
#   Authors: Christoph Jaeggli
#   Institute: Insel Data Science Center, Insel Gruppe AG
#
#   MIT License
#   Copyright (c) 2020 Christoph Jaeggli
#
#   This program is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.


# Standard library
# Third party requirements
import spacy
# Local imports

# Constants
_NLP = spacy.load('de_core_news_sm')


class GermanLemmatizer:
    """Defines a personalized German lemmatizer.
    """

    def __init__(self):
        self._lemmatizer = _german_lemmatizer()

    def lemma(self, token):
        """Lemmatizes a word and returns the result."""
        lemmatizer = self._lemmatizer

        # Make it all lower case
        lemma = token.lower()

        # Replace ß by ss
        lemma = (
            lemma.replace("ß", "ss")
        )

        # Use personalized lemmatizer
        try:
            lemma = lemmatizer[lemma]
        except KeyError:
            lemma = lemma

        # # Use spacy lemmatizer for normalization
        # lemma = [lm.lemma_ for lm in _NLP.tokenizer(lemma)]
        # lemma = ' '.join(lemma)

        # Umlaut accents are removed and
        lemma = (
            lemma.replace("\xE4", "ae")
            .replace("\xF6", "oe")
            .replace("\xFC", "ue")
        )

        return lemma


def _german_lemmatizer():
    """Returns a german dictionary with normalized words."""

    dict_ = {
        # A

        # - K -
        'kunden':                   'kunde',
        
        # - M -
        'mitarbeitend':             'mitarbeiter/in',
        'mitarbeitende':            'mitarbeiter/in',
        'mitarbeitenden':           'mitarbeiter/in',

        'mitarbeiterin':            'mitarbeiter/in',
        'mitarbeiterinnen':         'mitarbeiter/in',

    }

    return dict_


if __name__ == '__main__':
    print('\n')
    print('The total number of keys in the dictionary is')
    print(f'    --> {len(_german_lemmatizer().keys())} <--')
