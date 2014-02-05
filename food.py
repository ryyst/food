#! /usr/bin/python3.3
'''
Simple menuprinter for Unica and Sodexo student restaurants in Turku, Finland.

Python 3.3 required.

Script by Risto Puolakainen
'''


######## CONFIGURATION ########

sodexo_all = ['ict', 'eurocity', 'oldmill', 'lemminkaisenkatu']
unica_all  = ['assarin-ullakko', 'brygge', 'delica', 'deli-pharma', 'dental', 'macciavelli',
              'mikro', 'nutritio', 'ruokakello', 'tottisalmi', 'myssy-silinteri' ]

sodexo_default = 'ict'
unica_default  = 'delica'
# Default values without any flags. Can be anything you find in the above lists

lang = 'FI'
# EN or FI

###############################


def main():

    # TODO: Parse Sodexo json here
    # TODO: Parse Unica html here

    # TODO: Print food menu according to user input flags

    print()

if __name__ == '__main__':
    main()
