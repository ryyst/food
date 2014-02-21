######## CONFIGURATION ########

# List of all supported restaurants, omits a few weird ones.
# Editing these is possible but not intended, might have unintented side-effects.
# Edit default values instead.
#
SODEXO_ALL = ['ict', 'eurocity', 'oldmill', 'lemminkaisenkatu']
UNICA_ALL  = ['assarin-ullakko', 'brygge', 'delica', 'deli-pharma', 'dental', 'macciavelli',
              'mikro', 'nutritio', 'ruokakello', 'tottisalmi', 'myssy-silinteri' ]

# Default restaurants to be printed, you can add as many as you like. Use the lists
# above as a reference for editing these values. The format must be an exact match.
#
SODEXO_DEFAULTS = ['ict']
UNICA_DEFAULTS  = ['delica']

# Set your preferred language, either 'en' or 'fi'.
#
# NOTE! Sometimes, Unica english might have an empty menu while finnish one is not.
# This is a fault in their system and nothing end users can do about it.
#
LANG = 'fi'

# Do you want to use ANSI-coded text, colors, bold/underline etc.
# Either True or False
#
USE_EFFECTS = True

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
