# -*- coding: utf-8 -*-
""" Paths for the different folders.
"""

# Standard library
from pathlib import Path
# Third party requirements
# Local imports

# Path for the project's root directory
PATH_ROOT = Path(__file__).parents[1]

# # Path to the data folders
PATH_DATA           = Path(PATH_ROOT, 'data')
PATH_DATA_RAW       = Path(PATH_DATA, 'raw')
PATH_DATA_PROCESSED = Path(PATH_DATA, 'processed')

# Path to the model folder
PATH_MODELS         = Path(PATH_ROOT, 'models')

# Path to the figures
PATH_REP            = Path(PATH_ROOT, 'reports')
PATH_REP_DAT        = Path(PATH_REP, 'data')
PATH_REP_FIG        = Path(PATH_REP, 'figures')
PATH_REP_HTML       = Path(PATH_REP, 'html')
PATH_REP_PDF        = Path(PATH_REP, 'pdf')
PATH_REP_TEMPL      = Path(PATH_REP, 'templates')

# Path to src
PATH_SRC            = Path(PATH_ROOT, 'src')
PATH_SRC_DATA       = Path(PATH_SRC, 'data')


if __name__ == '__main__':
    print('\nRoot        -', PATH_ROOT, end='\n\n')

    print('Data        -', PATH_DATA)
    print('Data Raw    -', PATH_DATA_RAW)
    print('Data Proc   -', PATH_DATA_PROCESSED, end='\n\n')

    print('Models      -', PATH_MODELS, end='\n\n')

    print('Report      -', PATH_REP)
    print('Figures     -', PATH_REP_FIG, end='\n\n')

    print('Source      -', PATH_SRC)
    print('Source Data -', PATH_SRC_DATA, end='\n')
