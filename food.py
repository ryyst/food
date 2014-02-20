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
UNICA_DEFAULTS  = ['assarin-ullakko', 'brygge', 'delica', 'deli-pharma', 'dental', 'macciavelli',
              'mikro', 'nutritio', 'ruokakello', 'tottisalmi', 'myssy-silinteri' ]

# Set your preferred language, either 'en' or 'fi'.
#
# NOTE! Sometimes, Unica english might have an empty menu while finnish one is not.
# This is a fault in their system and nothing end users can do about it.
#
LANG = 'fi'


############ CODE #############

def get_sodexo_json():
    pass

def get_unica_html(unica_base):
    '''
    Form the proper URLs from Unica defaults and return all wanted HTML pages
    '''
    unica_data = []
    lang_jinxer = 'fi/ravintolat/' if LANG.lower() == 'fi' else 'en/restaurants/'

    for site in UNICA_DEFAULTS:
        unica_url = unica_base + lang_jinxer + site + '/'
        unica_data.append(str(web.urlopen(unica_url).read()))

    return unica_data

def main():
    sodexo_url = 'http://www.sodexo.fi/ruokalistat/output/daily_json/'
    unica_url  = 'http://www.unica.fi/'

    unica_data = get_unica_html(unica_url)

    unica_menu = {}
    for site, name in zip(unica_data, UNICA_DEFAULTS):
        print(name.capitalize())
        unica_menu[name] = parse_unica_html(site)

    # TODO: Parse Sodexo json here
    # TODO: Argparse
    # TODO: Error handling
    # TODO: Print food menu according to user input flags


if __name__ == '__main__':
    main()
