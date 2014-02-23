'''
All miscellaneous stuff goes here, in no particular order
'''
from datetime import datetime, timedelta

from config import *


if (LANG.lower() == 'en'):
    WEEK = { 0:'Monday', 1:'Tuesday', 2:'Wednesday',
             3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
else:
    WEEK = { 0:'Maanantai', 1:'Tiistai', 2:'Keskiviikko',
             3:'Torstai', 4:'Perjantai', 5:'Lauantai', 6:'Sunnuntai'}


def effect(content, effect):
    '''
    Wraps strings in ANSI-codes easily, if user has USE_EFFECTS enabled
    '''
    if USE_EFFECTS:
        return '%s%s%s' % (EFFECTS[effect.upper()], content, EFFECTS['RESET'])
    else:
        return content


def get_current_weekdates():
    now = datetime.today()
    start_date = now - timedelta(now.weekday())
    return [date for date in (start_date + timedelta(d) for d in range(7))]
