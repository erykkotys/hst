import hst
import datetime


def menu():
    while True:
        print('Wyszukiwarka niescislosci emisyjnych\n'
              'Wpisz:\n'
              '1. Analiza pojedynczego dnia\n'
              '2. Analiza zakresu dat\n'
              '3. Zakoncz dzialanie programu')
        select = input()
        if select == '1':
            user_input = date_input()
            file_1 = hst.HstFile(user_input)
            inconsistencies = file_1.get_inconsistencies()
            for inconsistency in inconsistencies:
                print(inconsistency)
            exit()
        elif select == '2':
            batch_search()
            exit()
        elif select == '3':
            exit()
        else:
            continue


def date_input(date_type='date', search_type='sprawdzic niescislosci'):
    while True:
        print(f'Podaj {date_type} w ktorej chcesz {search_type} w formacie YYYYMMDD (np. 20200415):')
        user_input = input()
        if user_input.isdigit() is True and len(user_input) == 8:
            break
        else:
            continue
    return user_input


def batch_search():
    while True:
        start_date = date_input('poczatkowa date')
        end_date = date_input('koncowa date')
        start_datetime = datetime.datetime.strptime(start_date, '%Y%m%d')
        end_datetime = datetime.datetime.strptime(end_date, '%Y%m%d')
        if start_datetime > end_datetime:
            continue
        else:
            break
    search_datetime = start_datetime
    increment = datetime.timedelta(days=1)
    while search_datetime != end_datetime:
        search_date = search_datetime.strftime('%Y%m%d')
        file = hst.HstFile(search_date)
        print(f'\nWyniki dla pliku {file.path} z {file.date.strftime("%Y-%m-%d (%A)")}: \n')
        inconsistencies = file.get_inconsistencies()
        if not inconsistencies:
            print('Brak dziur - emisja spojna')
        for inconsistency in inconsistencies:
            print(inconsistency)
        search_datetime += increment

    print('\n\n')


if __name__ == '__main__':
    menu()
