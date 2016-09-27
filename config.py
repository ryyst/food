######## CONFIGURATION ########
import sys
#
#
# List of all supported restaurants in Turku, omitting a few weird ones.
# Editing these is possible but not intended, might have unintented side-effects.
# Edit default values instead.
#
# If you want to get more sodexo restaurants, remember to include its restaurant id.
# (you can get this from their JSON page URLs)
#
SODEXO_ALL = {'ict': 54, 'eurocity': 23, 'oldmill': 70, 'lemminkaisenkatu': 64}
UNICA_ALL  = (
    'assarin-ullakko', 'brygge', 'delica', 'deli-pharma', 'dental', 'macciavelli',
    'mikro', 'nutritio', 'ruokakello', 'tottisalmi', 'myssy-silinteri'
)

# Default restaurants to be printed, you can add as many as you like. Use the lists
# above as a reference for editing these values. The format must be an exact match.
#
SODEXO_DEFAULTS = ['ict']
UNICA_DEFAULTS  = ['delica']

# Set your preferred language, either 'en' or 'fi'.
#
# NOTE! English versions are often not as complete as finnish ones (sometimes
# even missing completely). If this  bothers you, you should send an email to
# Sodexo and/or Unica. There's nothing else we can do about it.
#
LANG = 'fi'

# Set the price level to be printed.
# Possible values are 'student', 'employee', 'other'
#
PRICE_LEVEL = 'student'

# Do you want to see the whole week by default, instead of just today.
# Either True or False
#
PRINT_WHOLE_WEEK = True

# Do you want to use ANSI-coded text, colors, bold/underline etc.
# Windows users probably want to turn this off.
# Either True or False
#
USE_EFFECTS = True

# Colors and effects used for printing.
# You can play around with these if you want to.
#
EFFECTS = {
    'BLACK'   : '\033[30m',
    'RED'     : '\033[31m',
    'GREEN'   : '\033[32m',
    'YELLOW'  : '\033[33m',
    'BLUE'    : '\033[34m',
    'MAGENTA' : '\033[35m',
    'CYAN'    : '\033[36m',
    'WHITE'   : '\033[37m',

    'BOLD'    : '\033[1m',
    'UNDERL'  : '\033[4m',

    'RESET'   : '\033[00m',
}

# Do you want to see status / debug messages.
# Either True or False.
#
VERBOSE = False

# Filename where to dump JSON cache.
# File is located in this script's directory by default.
#
# CACHE_DIR = '/home/yourusername/'
CACHE_DIR = sys.path[0] + '/'

CACHE_FILE = CACHE_DIR + '.food.json'
