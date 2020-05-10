import hst

while True:
    print('Podaj date szukanego utworu w formacie YYYYMMDD (np. 20200415):')
    date = input()
    if date.isdigit() and len(date) == 8:
        try:
            file = hst.HstFile(date)
            break
        except FileNotFoundError:
            print('Plik o podanej dacie nie istnieje')
            continue
    else:
        print('Nieprawidlowy format daty')
        continue

while True:
    print('Podaj godzine w formacie HH:MM (np. 20:15):')
    time = input()
    if time[0:2].isdigit() and time[3:5].isdigit() and time[2]==':' and len(time) == 5:
        break
    else:
        print('Nieprawidlowy format czasu')
        continue

file.search(time)

