#!/usr/bin/python3.3
'''
Simple menuprinter for Unica and Sodexo student restaurants in Turku, Finland.

Python 3.3 required.

Script by Risto Puolakainen
'''
import urllib.request as web

from config import *
from parsers import *
from output import *


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
        unica_menu[name] = parse_unica_html(site)

    print_food(unica_menu)

    # TODO: Parse Sodexo json here
    # TODO: Argparse
    # TODO: Error handling
    # TODO: Print food menu according to user input flags


if __name__ == '__main__':
    main()
