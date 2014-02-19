'''
Parsing restaurant web data goes here
'''
from bs4 import BeautifulSoup, NavigableString, Tag
import re

def clean(data):
    '''
    Clear out the escape characters unica html contains and
    convert finnish characters that BS fails with
    '''

    if '\\xe2\\x82\\xac' in data:
        data = data.replace('\\xe2\\x82\\xac', '€')

    if '\\xc3\\xb6' in data:
        data = data.replace('\\xc3\\xb6', 'ö')

    if '\\xc3\\xa4' in data:
        data = data.replace('\\xc3\\xa4', 'ä')

    if '\\t' in data:
        data = data.replace('\\t', '')

    if '\\n' in data:
        data = data.replace('\\n', '')

    return data

def parse_unica_html(data):
    parser = BeautifulSoup(data)
    raw_menu = parser.find_all('div', {'class': 'accord'})

    week_menu = {}

    for data in raw_menu:

        # Start with day, taken from the html itself
        day = data.h4['data-dayofweek']
        print(day) #FIXME

        for food in data.table('tr'):

            # Nice generator to avoid further indentation
            only_tags = (food_tag for food_tag in food if isinstance(food_tag, Tag))
            food = Food()
            for tag in only_tags:

                if 'lunch' in tag['class']:
                    food.name = clean(tag.string)

                # Food properties like VEG, G or L
                if 'limitations' in tag['class']:
                    for limit in tag('span'):
                        food.properties.append(limit.string)
                
                if 'price' in tag['class']:
                    food.prices = re.findall('\d,\d\d', tag.string)

            print(food)

    week_menu[day] = data #FIXME
    restaurant = parser.find('div', {'class': 'head'}).h1.string
        #for child in data.descendants:
            #print(child)
        

    #print(week_menu)

class Food:
    def __init__(self, name="Undefined"):
        self.name = name
        self.prices = []
        self.properties = []

    def __str__(self):
        if self.properties:
            props = ','.join(self.properties)
            return '[ %s ] %s (%s)' % (self.prices[0], self.name, props)
        else:
            return '[ %s ] %s' % (self.prices[0], self.name)

