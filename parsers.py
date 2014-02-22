'''
Parsing restaurant web data goes here
'''
import re

from bs4 import BeautifulSoup, Tag

def parse_unica_html(site):
    parser = BeautifulSoup(site)
    html_menu = parser.find_all('div', {'class': 'accord'})

    week_menu = {}

    for day in html_menu:

        day_of_week = int(day.h4['data-dayofweek'])
        days_foods = []

        for food in day.table('tr'):

            try:
                # Nice generator to avoid further indentation
                only_tags = (food_tag for food_tag in food if isinstance(food_tag, Tag))
                food = Food()
                for tag in only_tags:

                    if 'lunch' in tag['class']:
                        food.name = tag.string

                    # Food properties like VEG, G or L
                    if 'limitations' in tag['class']:
                        for limit in tag.stripped_strings:
                            limit = limit
                            if limit == '/':
                                food.properties.append('/')
                            elif limit:
                                food.properties.append(limit)

                    if 'price' in tag['class']:
                        food.prices = re.findall('\d,\d\d', tag.string)

                days_foods.append(food)

            except:
                pass

        week_menu[day_of_week] = days_foods

    return week_menu


class Food:
    def __init__(self, name="Undefined"):
        self.name = name
        self.prices = []
        self.properties = []

    def __str__(self):
        if self.properties:
            props = ' '.join(self.properties)
            return '[ %s ] %s (%s)' % (self.prices[0], self.name, props)
        else:
            return '[ %s ] %s' % (self.prices[0], self.name)

