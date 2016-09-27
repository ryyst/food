'''
All miscellaneous stuff goes here, in no particular order
'''
from datetime import datetime, timedelta

import config


DAYS = {
    'en': [
        'Monday', 'Tuesday', 'Wednesday', 'Thursday',
        'Friday', 'Saturday', 'Sunday'
    ],
    'fi': [
        'Maanantai', 'Tiistai', 'Keskiviikko', 'Torstai',
        'Perjantai', 'Lauantai', 'Sunnuntai'
    ]
}
WEEK = dict(enumerate(DAYS[config.LANG.lower()]))


def ansify(content, effect):
    '''
    Wraps strings in ANSI-codes easily, if user has USE_EFFECTS enabled
    '''
    if config.USE_EFFECTS:
        return '%s%s%s' % (
            config.EFFECTS[effect.upper()],
            content,
            config.EFFECTS['RESET']
        )
    return content


def get_current_weekdates():
    now = datetime.today()
    start_date = now - timedelta(now.weekday())
    return [date for date in (start_date + timedelta(d) for d in range(7))]


def verbose_print(string):
    if config.VERBOSE:
        print('[DEBUG] %s' % string)
