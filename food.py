#!/usr/bin/python3.3
'''
Simple foodprinter for Unica and Sodexo student restaurants in Turku, Finland.

Python 3.3 required.

Script by Risto Puolakainen
'''
import urllib.request as web
from datetime import datetime, timedelta

from config import *
from parsers import *
from output import *


def get_current_weekdates():
    now = datetime.today()
    start_date = now - timedelta(now.weekday())
    return [date for date in (start_date + timedelta(d) for d in range(7))]


def get_sodexo_json(sodexo_base):
    '''
    Form the proper URLs from Sodexo defaults and return all wanted JSON data
    '''
    week_dates = get_current_weekdates()
    sodexo_data = list()

    for restaurant in SODEXO_DEFAULTS:
        print(restaurant)
        for date in week_dates:
            sodexo_url = '%s%s/%s/%s/%s/fi' % (sodexo_base, SODEXO_ALL[restaurant],
                                               date.year, date.month, date.day)
            sodexo_data.append(str(web.urlopen(sodexo_url).read().decode('utf8')))

    return sodexo_data


def get_unica_html(unica_base):
    '''
    Form the proper URLs from Unica defaults and return all wanted HTML pages
    '''
    # Default to 'fi', even with wrong configuration
    lang_jinxer = 'en/restaurants/' if LANG.lower() == 'en' else 'fi/ravintolat/'
    unica_data = list()

    for site in UNICA_DEFAULTS:
        unica_url = unica_base + lang_jinxer + site + '/'
        unica_data.append(str(web.urlopen(unica_url).read().decode('utf8')))

    return unica_data


def main():
    '''
    1. Initiate argparse
    2. Fetch all data from web
    3. Parse data
    4. Print data

    Specific configurations and flags have to be considered in every step,
    because we are using two websites that work totally differently.
    '''
    sodexo_url = 'http://www.sodexo.fi/ruokalistat/output/daily_json/'
    unica_url  = 'http://www.unica.fi/'

    unica_data = get_unica_html(unica_url)
    sodexo_data = get_sodexo_json(sodexo_url)
    #print(sodexo_data, "\n\n")

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
