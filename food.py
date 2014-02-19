#!/usr/bin/python3.3
'''
Simple menuprinter for Unica and Sodexo student restaurants in Turku, Finland.

Python 3.3 required.

Script by Risto Puolakainen
'''
import urllib.request as web

from parsers import *


######## CONFIGURATION ########

# List of all supported restaurants, omits a few weird ones.
# Editing these is possible but not intended, edit default values instead.
SODEXO_ALL = ['ict', 'eurocity', 'oldmill', 'lemminkaisenkatu']
UNICA_ALL  = ['assarin-ullakko', 'brygge', 'delica', 'deli-pharma', 'dental', 'macciavelli',
              'mikro', 'nutritio', 'ruokakello', 'tottisalmi', 'myssy-silinteri' ]

# Default values without any flags. Use the lists above as a reference
# for editing these defaults. The format must be an exact match.
SODEXO_DEFAULTS = ['ict']
UNICA_DEFAULTS  = ['delica', 'assarin-ullakko']

# Set your preferred language, either 'en' or 'fi'.
LANG = 'fi'

# You shouldn't have to edit these either.
SODEXO_BASE_URL = 'http://www.sodexo.fi/ruokalistat/output/daily_json/'
UNICA_BASE_URL  = 'http://www.unica.fi/'


############ CODE #############

def get_sodexo_json():
    pass

def get_unica_html():
    unica_data = []
    lang_jinxer = 'fi/ravintolat/' if LANG.lower() == 'fi' else 'en/restaurants/'

    for site in UNICA_DEFAULTS:
        unica_url = UNICA_BASE_URL + lang_jinxer + site + '/'
        unica_data.append(str(web.urlopen(unica_url).read()))

    return unica_data

def main():

    unica_data = get_unica_html()

    for page in unica_data:
        parse_unica_html(page)

    # TODO: Parse Sodexo json here
    # TODO: Parse Unica html here

    # TODO: Print food menu according to user input flags


if __name__ == '__main__':
    main()
