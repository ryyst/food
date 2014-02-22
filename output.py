'''
Food printing logic goes here
'''
from datetime import datetime
from config import *

if (LANG.lower() == 'en'):
    WEEK = { 0:'Monday', 1:'Tuesday', 2:'Wednesday',
             3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
else:
    WEEK = { 0:'Maanantai', 1:'Tiistai', 2:'Keskiviikko',
             3:'Torstai', 4:'Perjantai', 5:'Lauantai', 6:'Sunnuntai'}


def print_all(food_data):
    '''
    Print everything from every restaurant from every day
    '''
    for restaurant, week_menu in food_data.items():
        print(effect(restaurant.capitalize(), 'green'))
        failcount = 0
        for day, day_menu in week_menu.items():
            if not day_menu:
                failcount += 1
                print(effect("Nothing found for %s!" % WEEK[day], 'magenta'))
            else:
                if datetime.weekday(datetime.now()) == day:
                    print(effect('%s %s' % (WEEK[day], '(today)'), 'red'))
                else:
                    print(effect(WEEK[day], 'magenta'))

                for food in day_menu:
                    print(food)

        if failcount > 4 and LANG.lower() == 'en' and restaurant in UNICA_ALL:
            print("Maybe Unica is being lazy with their english site again?")


def print_today(food_data):
    '''
    Print only the current day from every selected restaurant.
    This should be the default action.
    '''
    today = datetime.weekday(datetime.now())
    print(effect(effect("TODAY'S MENU:", 'red'), 'bold'))

    for restaurant, week_menu in food_data.items():

        print(effect(restaurant.capitalize(), 'green'))
        try:
            for food in week_menu[today]:
                print(food)
        except:
            print('Nothing for today!')


def print_food(food_data):
    '''
    Main function for figuring out which stuff to print in what way
    '''
    print_all(food_data)


def effect(content, effect):
    '''
    Wraps strings in ANSI-codes easily, if user has USE_EFFECTS enabled
    '''
    if USE_EFFECTS:
        return '%s%s%s' % (EFFECTS[effect.upper()], content, EFFECTS['RESET'])
    else:
        return content

