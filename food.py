#!/usr/bin/python3.3
'''
Simple foodprinter for Unica and Sodexo student restaurants in Turku, Finland.

Requires Python3.3 and beautifulsoup4
'''
import urllib.request as web
import json
import os
import datetime

from common import *
from config import *
from output import *
from parsers import *

__author__ = 'Risto Puolakainen'


def main():
    '''
    1. Initiate argparse        - Missing
    2. Fetch all data from web/cache
    3. Parse data
    4. Print data

    Specific configurations and flags have to be considered in every step,
    because we are using two websites that work totally differently.
    '''
    food_menu = try_loading_cache()

    if not food_menu:
        food_data = download_data_from_web()
        food_menu = parse_food_data(food_data)
        cache_food_data(food_menu)

    print_food_menu(food_menu)

    # TODO: Argparse


#*********************** CACHING ***********************#
def try_loading_cache():
    '''
    Try to load CACHE_FILE and return it as string
    If not possible, then return None
    '''
    if not is_cache_uptodate():
        return None

    try:
        with open(CACHE_FILE, 'r') as f:
            data = ''
            for line in f:
                data += line
            food_menu = json.loads(data)

    except ValueError:
        verbose_print('Cache is broken!')
        return None


    return food_menu
    

def is_cache_uptodate():
    '''
    Check if cache exists and compare CACHE_FILE modify date to current weekdates
    '''
    try:
        mtime = os.path.getmtime(CACHE_FILE)

    except FileNotFoundError:
        verbose_print('No cache found!')
        return False


    mdate = datetime.fromtimestamp(mtime)
    for week_date in get_current_weekdates():
        if mdate.day == week_date.day:
            verbose_print('Cache is up to date!')
            return True

    verbose_print('Cache is NOT up to date!')
    return False


def cache_food_data(data):
    with open(CACHE_FILE, 'w') as outfile:
        json.dump(data, outfile, sort_keys=True, ensure_ascii=False, indent=2)


#********************* DOWNLOADING *********************#
def download_data_from_web():
    print('Fetching data from the web...')

    return { 'sodexo': get_sodexo_json(), 'unica': get_unica_html() }


def get_sodexo_json():
    '''
    Form the proper URLs from SODEXO_DEFAULTS and return all wanted JSON data
    '''
    sodexo_base = 'http://www.sodexo.fi/ruokalistat/output/daily_json/'

    week_dates = get_current_weekdates()
    sodexo_data = dict()
    
    for restaurant in SODEXO_DEFAULTS:
        verbose_print('Fetching Sodexo: %s...' % restaurant)

        sodexo_data[restaurant] = list()
        for date in week_dates:
            sodexo_url = '%s%s/%s/%s/%s/fi' % (sodexo_base, SODEXO_ALL[restaurant],
                                               date.year, date.month, date.day)
            sodexo_data[restaurant].append(str(web.urlopen(sodexo_url).read().decode('utf8')))

    return sodexo_data


def get_unica_html():
    '''
    Form the proper URLs from UNICA_DEFAULTS and return all wanted HTML pages
    '''
    unica_base = 'http://www.unica.fi/'

    # Default to 'fi', even with wrong configuration
    lang_jinxer = 'en/restaurants/' if LANG.lower() == 'en' else 'fi/ravintolat/'
    unica_data = dict()

    for restaurant in UNICA_DEFAULTS:
        verbose_print('Fetching Unica: %s...' % restaurant)

        unica_url = '%s%s%s/' % (unica_base, lang_jinxer, restaurant)
        unica_data[restaurant] = str(web.urlopen(unica_url).read().decode('utf8'))

    return unica_data


if __name__ == '__main__':
    main()
