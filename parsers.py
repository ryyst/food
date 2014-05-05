'''
Parsing restaurant web data goes here
'''
import re
import json

from bs4 import BeautifulSoup, Tag

import config
from common import *


def parse_food_data(data):
    verbose_print('Parsing data...')

    unica_menu = dict()
    for restaurant, week_html in data['unica'].items():
        verbose_print('Parsing Unica: %s...' % restaurant)

        unica_menu[restaurant] = parse_unica_html(week_html)

    sodexo_menu = dict()
    for restaurant, week_json in data['sodexo'].items():
        verbose_print('Parsing Sodexo: %s...' % restaurant)

        sodexo_menu[restaurant] = parse_sodexo_json(week_json)

    # Avoid putting empty data in the dictionary
    food_data = dict()
    if sodexo_menu:
        food_data['sodexo'] = sodexo_menu
    if unica_menu:
        food_data['unica'] = unica_menu

    return food_data


def parse_unica_html(html):
    parser = BeautifulSoup(html)
    html_week = parser.find_all('div', {'class': 'accord'})

    week_menu = dict()

    for day in html_week:

        day_of_week = str(day.h4['data-dayofweek'])
        day_menu = list()

        for food_data in day.table('tr'):

            # Filter out non-tags
            only_tags = [food_tag for food_tag in food_data if isinstance(food_tag, Tag)]

            if len(only_tags) < 3: #TODO! maybe get rid of this
                # Trying to fix a bug which breaks a whole day due to a notification.
                # In the end it was because of Unica's website had two closing
                # tags mixed up, so beautifulsoup can't parse rest of the day.
                # If they fix the mixup, then this code *should* simply skip the notification.
                continue

            food = dict()
            food['props'] = list()
            food['prices'] = list()
            for tag in only_tags:

                if 'lunch' in tag['class']:
                    food['name'] = tag.string

                # Food properties like VEG, G or L
                if 'limitations' in tag['class']:
                    for limit in tag.stripped_strings:
                        limit = limit
                        if limit == '/':
                            food['props'].append('/')
                        elif limit:
                            food['props'].append(limit)

                if 'price' in tag['class']:
                    food['prices'] = re.findall('\d\d,\d\d|\d,\d\d', tag.string)

            day_menu.append(food)

        week_menu[day_of_week] = day_menu

    return week_menu


def parse_sodexo_json(week_json):
    week = [json.loads(day) for day in week_json]

    week_menu = dict()
    for day_of_week, day in enumerate(week):
        day_of_week = str(day_of_week)
        day_menu = list()

        if not day['courses']: # Skip empty days
            continue

        for food_data in day['courses']:
            try:
                food = dict()
                food['props'] = list()
                food['prices'] = list()
                if config.LANG.lower() == 'en':
                    food['name'] = food_data['title_en']
                else:
                    food['name'] = food_data['title_fi']

                food['prices'] = re.findall('\d\d,\d\d|\d,\d\d', food_data['price'])

                try:
                    food['props'] = [prop.strip() for prop in food_data['properties'].split(',')]
                except:
                    pass # This is for when Sodexo JSON lacks 'properties'

                if food_data['category'].lower() == 'kasvislounas':
                    food['props'].append('VEG')
                
                day_menu.append(food)

            except:
                pass # This is for when days run out, usually on saturday.

        week_menu[day_of_week] = day_menu

    return week_menu
