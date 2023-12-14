import os
import json
import sys
import datetime
import re


class File:
    def __init__(self, file_path):
        self.file_path = open(file_path, 'r', encoding='utf-8')
        self.file_info = self.header()
        # self.json_file()

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
            # while header_line is None:
            #     break
            key = header_line[0]
            value = header_line[1] if len(header_line) > 1 else None
            file_info.update({key: value})
            header_line = next(self.file_path).split('"')[1::2]
        return file_info

    def json_file(self):
        if not os.path.exists('./json'):
            os.mkdir('./json')
        file_name = os.path.join('./json/', self.formatted_datatime + ' ' + self.file_info.get('Company') + '.json')
        with open(file_name, "w", encoding="cp1250", errors="xmlcharrefreplace") as json_file:
            json.dump(self.file_info, json_file, indent=2)

    @property
    def formatted_datatime(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H.%M.%S")


class Line(File):
    def __init__(self):
        pass


file = File('krawedzie.geo')
# file = File('GRZ-25511-27300.geo')
# file = File('krawedzie3.geo')
# file = File('1.geo')
# file = File('Chorzew_T5_spód_tłucznia.geo')
# file = File('Chorzew_T5_spód_tłucznia v2.geo')
# file = File('lk zegrze.geo')
# file = File('ŚR i CH.geo')

# print(str(file))


def generate_line_names_points():
    line_point = []
    for _ in file:
        print(_)
        if line_point_pattern.match(_):
            print(line_point_pattern.match(_))
            line_point.append(line_point_pattern.match(_).groupdict())
        elif _ == '\tend':
            return line_point


line_pattern = re.compile(r'\tLine (".+"?)?(?:,(\d+|),)?,(.+)?')
line_point_pattern = re.compile(r'\t\t\tPoint(?: (?P<Number>".+"|))?,(?P<X>\d+\.\d+|\d+),(?P<Y>\d+\.\d+|\d+),'
                                r'(?P<Z>\d+\.\d+|-\d+\.\d+|\d+)?(?:,"(?P<Code>.*?)")?,?')

for line in file:
    line_points = []
    print(line)
    if line_pattern.match(line):
        print(line_pattern.match(line)[1])
        line_points.extend(generate_line_names_points())
        print(line_points)
        # break
