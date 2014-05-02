'''
Food printing logic goes here
'''
from datetime import datetime

from common import *
from config import *

PRICE_LEVELS = [ 'student', 'employee', 'other' ]

def print_food_menu(menu):
    '''
    Main function for figuring out which stuff to print in what way
    '''
    # Get rid of unnecessary key(s), leaving only the companies.
    try:
        menu.pop('lang')
    except KeyError:
        pass

    verbose_print('Printing data...')

    if PRICE_LEVEL not in PRICE_LEVELS:
        print(ansify('Invalid PRICE_LEVEL value, defaulting back to student level.', 'red'))

    if PRINT_WHOLE_WEEK:
        print_all(menu)
    else:
        print_today(menu)


def format_food(food):

    # Default to student prices if user gives invalid PRICE_LEVEL
    if PRICE_LEVEL not in PRICE_LEVELS:
        price = food['prices'][0]

    else:
        for index, level in enumerate(PRICE_LEVELS):

            if level == PRICE_LEVEL:
                try:
                    price = food['prices'][index]

                except IndexError:
                    # This happens only if a restaurant doesn't have 3 price levels.
                    # We default to the highest price possible with the non-student
                    # values, because if they use these values they can't have student
                    # prices anyway. Student is always index 0 so it should never fail.
                    if PRICE_LEVEL == 'other' or 'employee':
                        try:
                            price = food['prices'][-1]

                        except IndexError:
                            # If there is no price level (probably still not free though)
                            price = " -- "

    props = '{%s}' % ' '.join(food['props']) if food['props'] else ''
    name = food['name'].capitalize()

    return '[ %s ] %s %s' % (price, name, props)


def print_all(food_menu):
    '''
    Print everything from every selected restaurant from every day
    '''
    week_dates = [date.strftime('%d.%m') for date in get_current_weekdates()]

    for corp, restaurant in sorted(food_menu.items()):
        for name, week_menu in sorted(restaurant.items()):

            print(ansify('%s (%s)' % (name.capitalize(), corp.capitalize()), 'green'))

            if not week_menu:
                print(ansify(' Nothing for the whole week!', 'magenta'))

                if LANG.lower() == 'en':
                    print("  Maybe %s is being lazy with their english menu again?" % corp.capitalize())
                    # This shit happens way too often

            for day, day_menu in sorted(week_menu.items()):
                day = int(day)
                if not day_menu:
                    print(ansify(' Nothing found for %s (%s)' % (WEEK[day], week_dates[day]), 'magenta'))

                else:
                    if datetime.weekday(datetime.now()) == day:
                        print(ansify(' %s (%s)' % (WEEK[day], 'today'), 'red'))
                    else:
                        print(ansify(' %s (%s)' % (WEEK[day], week_dates[day]), 'magenta'))

                    for food in day_menu:
                        print("  %s" % format_food(food))

            print() # Newline after every restaurant!


def print_today(food_menu):
    '''
    Print only the current day from every selected restaurant.
    This should be the default action.
    '''
    today_date = datetime.now().strftime('%d.%m.%y')
    print(ansify('%s (%s)' % ("Today's menu", today_date), 'red'))

    today = str(datetime.weekday(datetime.now()))

    for corp, restaurant in sorted(food_menu.items()):
        for name, week_menu in sorted(restaurant.items()):

            print(ansify(' %s (%s)' % (name.capitalize(), corp.capitalize()), 'green'))
            try:
                for food in week_menu[today]:
                    print("  %s" % format_food(food))
            except KeyError:
                print('  Nothing for today!')

        print() # Newline after every restaurant!
