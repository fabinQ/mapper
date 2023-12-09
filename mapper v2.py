import os
import json
import sys
import datetime


class File:
    def __init__(self, file_path):
        self.file_path = open(file_path, 'r', encoding='utf-8')
        self.file_info = self.header()
        self.json_file()

    def __next__(self):
        return next(self.file_path).rstrip()

    def __iter__(self):
        return self

    def __str__(self):
        return '\n'.join(f'{key} - {value}' for item in self.file_info for key, value in item.items())

    def header(self):
        file_info = {}
        header_line = tuple(next(self.file_path).split('"')[1::2])
        file_info.update({'Header': header_line})
        next(self.file_path)
        header_line = next(self.file_path).split('"')[1::2]
        while header_line:
            key = header_line[0]
            value = header_line[1] if len(header_line) > 1 else None
            file_info.update({key: value})
            header_line = next(self.file_path).split('"')[1::2]
        return file_info

    def json_file(self):
        file_name = os.path.join('./json/', self.formatted_datatime + ' ' + self.file_info.get('Company') + '.json')
        with open(file_name, "w", encoding="cp1250", errors="xmlcharrefreplace") as json_file:
            json.dump(self.file_info, json_file, indent=2)

    @property
    def formatted_datatime(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H.%M.%S")


# file = File('krawedzie.geo')
# file = File('GRZ-25511-27300.geo')
# file = File('1.geo')
file = File('Chorzew_T5_spód_tłucznia.geo')
# file = File('Chorzew_T5_spód_tłucznia v2.geo')
# file = File('lk zegrze.geo')
# file = File('ŚR i CH.geo')

# print(str(file))

for line in file:
    print(line)
