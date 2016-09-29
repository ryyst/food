'''
Parsing and working with cli arguments goes here
'''
import argparse
import config
import sys


def initiate_argparse():
    '''Create argparse with all the arguments AND parse them.'''

    desc = '''CLI for printing food of Sodexo / Unica restaurants in Turku.

You should edit config.py for your default settings.
Using these flags directly does not save or cache anything.'''

    epilog = '''
For more info visit: http://www.unica.fi/ and http://www.sodexo.fi/
'''

    parser = argparse.ArgumentParser(
        prog='food',
        description=desc,
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '-a', '--ansi',
        action='store_true',
        help='Toggle ANSI color coding.'
    )
    parser.add_argument(
        '-r', '--restaurants',
        action='store_true',
        help='List all restaurant options.'
    )
    parser.add_argument(
        '-t', '--today',
        action='store_true',
        help='Force "today" display mode.'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show debug messages.'
    )
    parser.add_argument(
        '-w', '--week',
        action='store_true',
        help='Force "week" display mode.'
    )

    parser.add_argument(
        '-s', '--sodexo',
        nargs='+',
        help='Specify which Sodexo restaurants to show'
    )
    parser.add_argument(
        '-u', '--unica',
        nargs='+',
        help='Specify which Unica restaurants to show'
    )
    parser.add_argument(
        '-l', '--language',
        choices=['en', 'fi'],
        help='Specify displayed language'
    )
    parser.add_argument(
        '-p', '--price',
        choices=['student', 'employee', 'other'],
        help='Specify displayed price level'
    )
    parser.add_argument(
        '-f', '--force',
        action='store_true',
        help='Force redownload of cache'
    )

    return parser.parse_args()


def execute_arguments(args):
    '''
    Execute all arguments and return an arg_override, for controlling cache logic.

    This function simply changes the values from config.py.
    This is not a good practice, but works for a project of this scope.
    '''
    arg_override = False

    if args.verbose:
        config.VERBOSE = True

    if args.ansi:
        config.USE_EFFECTS = not config.USE_EFFECTS

    if args.today:
        config.PRINT_WHOLE_WEEK = False

    if args.week:
        config.PRINT_WHOLE_WEEK = True

    if args.restaurants:
        print('Unica:', ", ".join(config.UNICA_ALL))
        print('Sodexo:', ", ".join(config.SODEXO_ALL.keys()))
        sys.exit(0)

    if args.sodexo:
        config.SODEXO_DEFAULTS = args.sodexo
        if not args.unica:
            config.UNICA_DEFAULTS = []  # Ignore any configs
        arg_override = True

    if args.unica:
        config.UNICA_DEFAULTS = args.unica
        if not args.sodexo:
            config.SODEXO_DEFAULTS = []  # Ignore any configs
        arg_override = True

    if args.language:
        config.LANG = args.language
        arg_override = True

    if args.price:
        config.PRICE_LEVEL = args.price

    return arg_override, args.force
