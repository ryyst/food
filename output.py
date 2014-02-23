'''
Food printing logic goes here
'''
from datetime import datetime

from common import *
from config import *


def print_food_menu(menu):
    '''
    Main function for figuring out which stuff to print in what way
    '''
    print_all(menu)
    #print_today(menu)


def print_all(food_menu):
    '''
    Print everything from every selected restaurant from every day
    '''
    week_dates = [date.strftime('%d.%m') for date in get_current_weekdates()]

    for corp, restaurant in food_menu.items():
        for name, week_menu in restaurant.items():

            print(effect('%s (%s)' % (name.capitalize(), corp.capitalize()), 'green'))
            failcount = 0

            for day, day_menu in week_menu.items():

                if not day_menu:
                    failcount += 1
                    print(effect("Nothing found for %s!" % WEEK[day], 'magenta'))

                else:
                    if datetime.weekday(datetime.now()) == day:
                        print(effect('%s (%s)' % (WEEK[day], 'today'), 'red'))
                    else:
                        print(effect('%s (%s)' % (WEEK[day], week_dates[day]), 'magenta'))

                    for food in day_menu:
                        print(food)

            if failcount > 4 and LANG.lower() == 'en' and restaurant in UNICA_ALL:
                print("Maybe Unica is being lazy with their english site again?")


def print_today(food_menu):
    '''
    Print only the current day from every selected restaurant.
    This should be the default action.
    '''
    today = datetime.weekday(datetime.now())
    today_date = datetime.now().strftime('%d.%m.%y')
    print(effect('%s (%s)' % ("TODAY'S MENU", today_date), 'red'))

    for corp, restaurant in food_menu.items():
        for name, week_menu in restaurant.items():

            print(effect('%s (%s)' % (name.capitalize(), corp.capitalize()), 'green'))
            try:
                for food in week_menu[today]:
                        print(food)
            except KeyError:
                print('Nothing for today!')
