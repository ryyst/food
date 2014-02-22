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


def get_sodexo_json():
    '''
    Form the proper URLs from Sodexo defaults and return all wanted JSON data
    '''
    sodexo_base = 'http://www.sodexo.fi/ruokalistat/output/daily_json/'

    week_dates = get_current_weekdates()
    sodexo_data = dict()
    
    #TODO: Make it get only one json by default
    for restaurant in SODEXO_DEFAULTS:
        sodexo_data[restaurant] = list()
        for date in week_dates:
            print(date)
            sodexo_url = '%s%s/%s/%s/%s/fi' % (sodexo_base, SODEXO_ALL[restaurant],
                                               date.year, date.month, date.day)
            sodexo_data[restaurant].append(str(web.urlopen(sodexo_url).read().decode('utf8')))

    return sodexo_data


def get_unica_html(unica_base):
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


def main():
    '''
    1. Initiate argparse
    2. Fetch all data from web
    3. Parse data
    4. Print data

    Specific configurations and flags have to be considered in every step,
    because we are using two websites that work totally differently.
    '''

    unica_html = get_unica_html(unica_url)
    sodexo_json = get_sodexo_json(sodexo_url)

    unica_menu = dict()
    for restaurant, week_html in unica_html.items():
        unica_menu[restaurant] = parse_unica_html(week_html)

    sodexo_menu = dict()
    for restaurant, week_json in sodexo_json.items():
        sodexo_menu[restaurant] = parse_sodexo_json(week_json)

    print_food(unica_menu)
    print_food(sodexo_menu)

    # TODO MAYBE: test user configs?
    # TODO: Argparse
    # TODO: Error handling
    # TODO: Print food menu according to user input flags


if __name__ == '__main__':
    main()
