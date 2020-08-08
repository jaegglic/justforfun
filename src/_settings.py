# -*- coding: utf-8 -*-
"""Definition of common settings.
"""

# Random seed
SEED = 25654

# Patterns for the nltk analysis
PATTERNS_OF_INTEREST = [
    r'mitarbeite(n|nd|r|rin|rinnen)',
    r'kunde[n]?',
]
DF_COL_YEAR = 'Year'
DF_COL_PROFIT = 'Profit'
DF_COL_NWORDS = 'NWords'
DF_COL_COUNT = 'Count_'
DF_COL_POL = 'Polarity_'

# Normalizing profit
PROFIT_NORMALIZATION = int(1e6)
PROFIT_UNIT = 'MSFr'

# Color definitions
CLR_BUSINESS_00 =       '#677078'    # Grey
CLR_BUSINESS_01 =       '#009870'    # Green
CLR_BUSINESS_02 =       '#6ca5da'    # Light Blue
CLR_BUSINESS_03 =       '#e5cbd6'    # Light Magenta
CLR_BUSINESS_04 =       '#ee8f7a'    # Light Red
CLR_BUSINESS_05 =       '#d1e2bc'    # Light Green
CLR_BUSINESS_06 =       '#e4dbcf'    # Light Brown
CLR_BUSINESS_07 =       '#8c7482'    # Magenta
CLR_BUSINESS_08 =       '#9b6051'    # Brown
CLR_BUSINESS_09 =       '#4a7094'    # Blue

CLR_CHART_01 =          '#004586'    # Dark blue
CLR_CHART_02 =          '#ff420e'    # Orange/Red
CLR_CHART_03 =          '#ffd320'    # Yellow
CLR_CHART_04 =          '#579d1c'    # Green
CLR_CHART_05 =          '#7e0021'    # Dark red
CLR_CHART_06 =          '#83caff'    # Light blue
CLR_CHART_07 =          '#314004'    # Dark green
CLR_CHART_08 =          '#aecf00'    # Light green
CLR_CHART_09 =          '#4b1f6f'    # Magenta
CLR_CHART_10 =          '#ff950e'    # Orange
CLR_CHART_11 =          '#c5000b'    # Red
CLR_CHART_12 =          '#0084d1'    # Blue

# Figure settings
LINEWIDTH = 4
MARKERSIZE = 12
FONTSIZE = 18