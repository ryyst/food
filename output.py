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
    if VERBOSE: print('Printing data...')

    if PRINT_WHOLE_WEEK:
        print_all(menu)
    else:
        print_today(menu)


def format_food(food):
    if food['props']:
        props = ' '.join(food['props'])
        return '[ %s ] %s (%s)' % (food['prices'][0], food['name'].capitalize(), props)
    else:
        return '[ %s ] %s' % (food['prices'][0], food['name'].capitalize())


def print_all(food_menu):
    '''
    Print everything from every selected restaurant from every day
    '''
    week_dates = [date.strftime('%d.%m') for date in get_current_weekdates()]

    for corp, restaurant in food_menu.items():
        for name, week_menu in restaurant.items():

            print(effect('%s (%s)' % (name.capitalize(), corp.capitalize()), 'green'))

            if not week_menu:
                print(effect(' Nothing for the whole week!', 'magenta'))

                if LANG.lower() == 'en':
                    print("  Maybe %s is being lazy with their english menu again?" % corp.capitalize())
                    # This shit happens way too often
                #continue

            for day, day_menu in week_menu.items():
                if not day_menu:
                    print(effect(' Nothing found for %s (%s)' % (WEEK[day], week_dates[day]), 'magenta'))

                else:
                    if datetime.weekday(datetime.now()) == day:
                        print(effect(' %s (%s)' % (WEEK[day], 'today'), 'red'))
                    else:
                        print(effect(' %s (%s)' % (WEEK[day], week_dates[day]), 'magenta'))

                    for food in day_menu:
                        print("  %s" % format_food(food))

            print() # Newline after every restaurant!


def print_today(food_menu):
    '''
    Print only the current day from every selected restaurant.
    This should be the default action.
    '''
    today = datetime.weekday(datetime.now())
    today_date = datetime.now().strftime('%d.%m.%y')
    print(effect('%s (%s)' % ("Today's menu", today_date), 'red'))

    for corp, restaurant in food_menu.items():
        for name, week_menu in restaurant.items():

            print(effect(' %s (%s)' % (name.capitalize(), corp.capitalize()), 'green'))
            try:
                for food in week_menu[today]:
                    print("  %s" % format_food(food))
            except KeyError:
                print('Nothing for today!')
