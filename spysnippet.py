import datetime
import os


class SpySnippet:

    spy_folder = r'S:'
    temp_file = os.path.join(r'L:\Wycinki ze Szpiega', 'temp.mp3')
    export_folder = r'L:\Wycinki ze Szpiega'
    allowed_length = datetime.timedelta(minutes=60)

    def __init__(self, date, time_start, time_end):
        self.start = datetime.datetime.strptime(date+time_start, '%Y%m%d%H:%M:%S')
        self.end = datetime.datetime.strptime(date+time_end, '%Y%m%d%H:%M:%S')
        if self.start > self.end:
            print('Dlugosc wycinka nie moze byc ujemna')
            exit()
        self.length = self.end - self.start
        if self.length > SpySnippet.allowed_length:
            print(f'Dlugosc wycinka nie moze przekraczac {SpySnippet.allowed_length}, a wynosi {self.length}')
            exit()
        if self.start.hour == self.end.hour:
            self.file = self.find_file(self.start)
        else:
            self.file = self.cat(self.start, self.end)

    def __str__(self):
        return f'start: {self.start}, end: {self.end}, length: {self.length}'

    @staticmethod
    def find_file(start_time):
        file_string = start_time.strftime('%Y %m %d %H 00 00')
        spy_file = ''
        for file in os.listdir(SpySnippet.spy_folder):
            if file.startswith(file_string):
                spy_file = os.path.join(SpySnippet.spy_folder, file)
        return spy_file

    def cat(self, start, end):
        # TODO: change this to __add__ method
        files = []
        while start.hour <= end.hour:
            file = self.find_file(start)
            files.append(file)
            start += datetime.timedelta(hours=1)
        with open(SpySnippet.temp_file, 'wb') as f:
            for file in files:
                with open(file, 'rb') as part:
                    part = part.read()
                    f.write(part)
        return SpySnippet.temp_file

    def cut(self):
        # 32000 bytes = 1 sec of 256kbps mp3
        chunk_size = 32000
        start_sec = self.start.minute*60+self.start.second
        end_sec = start_sec + self.length.total_seconds()
        export_file = os.path.join(SpySnippet.export_folder, f'{self.start.strftime("%Y%m%d_%H_%M_%S_-_")}'
                                                      f'{self.end.strftime("%H_%M_%S")}.mp3')
        with open(self.file, 'rb+') as f:
            chunk = f.read(chunk_size)
            with open(export_file, 'wb') as export:
                sec = 0
                while chunk:
                    if start_sec <= sec <= end_sec:
                        export.write(chunk)
                    chunk = f.read(chunk_size)
                    sec += 1
        os.unlink(SpySnippet.temp_file)
        print(f'\nPlik {export_file} zapisany prawidłowo')


if __name__ == '__main__':
    file_1 = SpySnippet('20200415', '20:12:15', '21:02:12')
    print(file_1)
    file_1.cut()
