import sys
from datos import *

def main():
    while True:
        print('PANDAS ACTIVITY - MAIN MENU')
        print('1. Prepare data')
        print('2. Save report')
        print('3. Show graphic')
        print('4. Exit')

        option = input('Choose an option: ').strip()

        if option == '1':
            data = prepare_data()
        elif option == '2':
            if data is not None:
                save_report(data)
        elif option == '3':
            if data is not None:
                show_graphic(data)
        elif option == '4':
            sys.exit()
        else:
            print('Invalid option. Please try again.')

if __name__ == '__main__':
    main()