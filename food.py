#!/usr/bin/python3.3
'''
Simple foodprinter for Unica and Sodexo student restaurants in Turku, Finland.

Requires Python3.3 and beautifulsoup4
'''
import urllib.request as web

from common import *
from config import *
from output import *
from parsers import *

__author__ = 'Risto Puolakainen'


def main():
    '''
    1. Initiate argparse
    2. Fetch all data from web
    3. Parse data
    4. Print data

    Specific configurations and flags have to be considered in every step,
    because we are using two websites that work totally differently.
    '''
    food_data = download_data_from_web()
    food_menu = parse_food_data(food_data)
    print_food_menu(food_menu)

    # TODO MAYBE: test user configs?
    # TODO: Argparse
    # TODO: Error handling
    # TODO: Print food menu according to user input flags


def download_data_from_web():
    print('Fetching data...')
    return { 'sodexo': get_sodexo_json(), 'unica': get_unica_html() }


def get_sodexo_json():
    '''
    Form the proper URLs from Sodexo defaults and return all wanted JSON data
    '''
    sodexo_base = 'http://www.sodexo.fi/ruokalistat/output/daily_json/'

    week_dates = get_current_weekdates()
    sodexo_data = dict()
    
    for restaurant in SODEXO_DEFAULTS:
        sodexo_data[restaurant] = list()
        for date in week_dates:
            sodexo_url = '%s%s/%s/%s/%s/fi' % (sodexo_base, SODEXO_ALL[restaurant],
                                               date.year, date.month, date.day)
            sodexo_data[restaurant].append(str(web.urlopen(sodexo_url).read().decode('utf8')))

    return sodexo_data


def get_unica_html():
    '''
    Form the proper URLs from Unica defaults and return all wanted HTML pages
    '''
    unica_base = 'http://www.unica.fi/'

    # Default to 'fi', even with wrong configuration
    lang_jinxer = 'en/restaurants/' if LANG.lower() == 'en' else 'fi/ravintolat/'
    unica_data = dict()

    for restaurant in UNICA_DEFAULTS:
        unica_url = '%s%s%s/' % (unica_base, lang_jinxer, restaurant)
        unica_data[restaurant] = str(web.urlopen(unica_url).read().decode('utf8'))

    return unica_data


if __name__ == '__main__':
    main()
