import datetime
import os
import chardet
import pyperclip


class HstFile:

    folder = r'K:\dynamix\hst'

    def __init__(self, date):
        self.date = datetime.datetime.strptime(date, '%Y%m%d')
        self.path = os.path.join(HstFile.folder, self.date.strftime('%y_%m_%d.HST'))
        self.content = self.get_content()
        self.entries = self.parse()

    def get_content(self):
        """
        Opens the file, tires find the appropriate encoding, read the file and return it's content
        """
        with open(self.path, "rb") as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
        if encoding:
            with open(self.path, 'r', encoding=encoding) as f:
                content = f.readlines()
        else:
            try:
                with open(self.path, 'r', encoding='ansi') as f:
                    content = f.readlines()
            except UnicodeDecodeError:
                print('Jakis blad kodowania pliku')
                return -1
        return content

    def parse(self):
        entries = []
        for i, line in enumerate(self.content):
            data = line.split('; ')
            entries.append(Entry(data[0] + data[2], data[1], data[3], data[4], data[5], data[6], data[7]))
        return entries

    def inconsistencies(self, margin_low=10, margin_high=20):
        margin_low = datetime.timedelta(seconds=margin_low)
        margin_high = datetime.timedelta(minutes=margin_high)
        inconsistencies = []
        # first entry always has incorrect date
        expected = self.entries[0].expected_end+datetime.timedelta(days=1)
        for entry in self.entries[1:]:
            time_diff = entry.time - expected
            if time_diff > margin_high:
                inconsistencies.append(f' * DUZA dziura w emisji (TRANSMISJA?), spodziewany czas {expected.time()}, '
                                       f'rzeczywisty: {entry.time}, roznica: {time_diff} * ')
            elif time_diff > margin_low:
                inconsistencies.append(f' * Dziura w emisji, spodziewany czas {expected.time()}, '
                                       f'rzeczywisty: {entry.time}, roznica: {time_diff} * ')
            expected = entry.time + entry.length
        for i in inconsistencies:
            print(i)
        return inconsistencies

    def search(self, time):
        time = datetime.timedelta(hours=int(time[0:2]), minutes=int(time[3:5]))
        search = self.date + time
        for i, entry in enumerate(self.entries):
            if entry.time < search < self.entries[i+1].time:
                print('-'*80, '\n')
                print(f'Utwór grany {search.date()} o {search.time()}:')
                print(entry)
                pyperclip.copy(f'{entry.artist} - {entry.title}')
                print('Utwor skopiowany do schowka, wcisnij Ctrl + V aby wkleic')
                print('\n', '-'*80)
                print('Kontekst:')
                for x in range(-3, 3):
                    print(self.entries[i+x])
                print('-'*80)
                return f'{entry.artist} - {entry.title}'


class Entry:

    def __init__(self, time, path, played, length, title, composer, artist):
        self.time = datetime.datetime.strptime(time, '%H:%M:%S%y_%m_%d')
        self.path = path
        self.played = int(played.strip('%'))*0.01
        self.length = datetime.timedelta(minutes=int(length[0:2]), seconds=int(length[3:5]))
        self.title = title
        self.composer = composer
        self.artist = artist
        self.expected_end = self.time + self.length

    def __str__(self):
        return f'{self.time} : {self.artist} - {self.title}'
