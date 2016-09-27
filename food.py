#!/usr/bin/python3
'''
Simple foodprinter for Unica and Sodexo student restaurants in Turku, Finland.

Requires Python3.3 and beautifulsoup4
'''
import urllib.request as web
import json
import sys
import os
from datetime import datetime

import config
from common import verbose_print, get_current_weekdates
from output import print_food_menu
from parsers import parse_food_data
from args import initiate_argparse, execute_arguments

__author__ = 'Risto Puolakainen'


def main():
    '''
    In simple terms:
    1. Initiate argparse
    2. Fetch all data from web/cache
    3. Parse data
    4. Print data

    Specific configurations and flags have to be considered in every step,
    because we are using two websites that work totally differently.
    '''
    args = initiate_argparse()
    arg_override = execute_arguments(args)
    food_menu = None

    if not arg_override:
        food_menu = try_loading_cache()

    # Check if we need to download the data.
    if not food_menu or is_config_modified_since_caching(food_menu, arg_override):
        food_data = download_data_from_web()
        food_menu = parse_food_data(food_data)
        if not arg_override:
            cache_food_data(food_menu)

    print_food_menu(food_menu)


#
# ********************************** CACHING ********************************** #
#
def is_config_modified_since_caching(food_menu, arg_override):
    '''
    Compare the cached data to current user configs in a few different ways.
    Check only restaurants and language, since others don't depend on the cache.
    '''
    # Don't do any of this stuff if certain arguments are used.
    if arg_override:
        return False

    try:
        config_restaurants = config.SODEXO_DEFAULTS + config.UNICA_DEFAULTS
    except TypeError:
        print('ERROR: You are using invalid format in your default restaurants.')
        print('If you want no restaurants put [] as value')
        sys.exit(1)

    rest_count = 0

    # Language must be checked because we cache only one
    if not food_menu['lang'] == config.LANG.lower():
        verbose_print("Cached language doesn't match configs")
        print("Configs have been changed since caching! Redownloading...")
        food_menu.pop('lang')
        return True
    food_menu.pop('lang')

    # The restaurants should be the same
    for restaurant in food_menu.values():
        for name in restaurant:
            if name not in config_restaurants:
                verbose_print("Cached restaurants are not the same as in config")
                print("Configs have been changed since caching! Redownloading...")
                return True
            rest_count += 1

    # The amount of restaurants should match
    if len(config_restaurants) != rest_count:
        verbose_print("The number of cached restaurants doesn't match with config")
        print("Configs have been changed since caching! Redownloading...")
        return True

    return False


def try_loading_cache():
    '''
    Try to load CACHE_FILE and return it as string
    If not possible, then return None
    '''
    if not is_cache_uptodate():
        return None

    try:
        with open(config.CACHE_FILE, 'r') as f:
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
        mtime = os.path.getmtime(config.CACHE_FILE)

    except FileNotFoundError:
        verbose_print('No cache found!')
        return False

    mdate = datetime.fromtimestamp(mtime)
    for week_date in get_current_weekdates():
        if mdate.day == week_date.day:
            verbose_print('Cache is from this week')
            return True

    verbose_print('Cache is not up to date')
    return False


def cache_food_data(data):
    data['lang'] = config.LANG.lower()
    with open(config.CACHE_FILE, 'w') as outfile:
        json.dump(data, outfile, sort_keys=True, ensure_ascii=False, indent=2)
    print('Data cached for the rest of the week!')


#
# ******************************** DOWNLOADING ******************************** #
#
def download_data_from_web():
    print('Fetching data from the web (this might take a while)...')
    return {'sodexo': get_sodexo_json(), 'unica': get_unica_html()}


def get_sodexo_json():
    '''
    Form the proper URLs from SODEXO_DEFAULTS and return all wanted JSON data
    '''
    sodexo_base = 'http://www.sodexo.fi/ruokalistat/output/daily_json/'

    week_dates = get_current_weekdates()
    sodexo_data = dict()

    try:
        for restaurant in config.SODEXO_DEFAULTS:
            verbose_print('Fetching Sodexo: %s...' % restaurant)

            sodexo_data[restaurant] = list()
            for date in week_dates:
                sodexo_url = '%s%s/%s/%s/%s/fi' % (
                    sodexo_base, config.SODEXO_ALL[restaurant],
                    date.year, date.month, date.day
                )
                sodexo_data[restaurant].append(str(web.urlopen(sodexo_url).read().decode('utf8')))
    except KeyError:
        print('ERROR: Invalid Sodexo restaurant specified.')
        print('Use -r flag to find out all the restaurants')
        sys.exit(1)

    return sodexo_data


def get_unica_html():
    '''
    Form the proper URLs from UNICA_DEFAULTS and return all wanted HTML pages
    '''
    unica_base = 'http://www.unica.fi/'

    # Default to 'fi', even with wrong configuration
    lang_jinxer = 'en/restaurants/' if config.LANG.lower() == 'en' else 'fi/ravintolat/'
    unica_data = dict()

    try:
        for restaurant in config.UNICA_DEFAULTS:
            verbose_print('Fetching Unica: %s...' % restaurant)

            unica_url = '%s%s%s/' % (unica_base, lang_jinxer, restaurant)
            unica_data[restaurant] = str(web.urlopen(unica_url).read().decode('utf8'))
    except:
        print('ERROR: Invalid Unica restaurant specified.')
        print('Use -r flag to find out all the restaurants')
        sys.exit(1)

    return unica_data


if __name__ == '__main__':
    main()
