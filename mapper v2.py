import os
import json
import sys
import datetime
import re
import pprint

class File:
    def __init__(self, file_path):
        self.data_time_stamp = self.formatted_datatime
        self.file_path = open(file_path, 'r', encoding='utf-8')
        self.file_info = self.header()
        self.file_name = './json/' + self.data_time_stamp + ' ' + self.file_info.get('Company') + '.json'
        # self.json_file(self.file_info, self.file_name)

    def __next__(self):
        return next(self.file_path).rstrip()

    def __iter__(self):
        return self

    def __str__(self):
        return self.file_path.name

    def header(self):
        file_info = {'File': File.__str__(self)}
        header_line = tuple(next(self.file_path).split('"')[1::2])
        file_info.update({'Header': header_line})
        next(self)
        header_line = next(self.file_path).split('"')[1::2]
        while header_line:
            # while header_line is None:
            #     break
            key = header_line[0]
            value = header_line[1] if len(header_line) > 1 else None
            file_info.update({key: value})
            header_line = next(self.file_path).split('"')[1::2]
        return file_info

    @staticmethod
    def json_file(content, file_name):
        if not os.path.exists('./json'):
            os.mkdir('./json')
        with open(file_name, "a", encoding="utf-8", errors="xmlcharrefreplace") as json_file:
            json.dump(content, json_file, indent=2)
            json_file.write('\n')

    @property
    def formatted_datatime(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H.%M.%S")


class Line(File):
    number_of_line = 0
    def __init__(self, line_id_class, line_point_class):
        file_name = file.file_name
        self.line_id_class = line_id_class
        self.line_point_class = line_point_class
        self.line_class = {'Info': self.line_id_class, 'PointList': self.line_point_class}
        # self.json_file(self.line_class, file_name)
        # number_of_line +=1

    def simplifier(self):
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
assert str(file).endswith('.geo')


def generate_line_names_points():
    line_point = []
    for _ in file:
        if line_point_pattern.match(_):
            line_point_dic = line_point_pattern.match(_).groupdict()
            line_point.append(line_point_dic)
        elif _ == '\tend':
            return line_point


# patterny do linii i punktów
line_pattern = re.compile(r'\tLine "(?P<ID_line>.+?)"?,(?P<Polygon>\d+|)?,(?P<Descriptoin>.+)?')
line_point_pattern = re.compile(r'\t\t\tPoint(?: "(?P<Number>.+|)")?,(?P<X>\d+\.\d+|\d+),(?P<Y>\d+\.\d+|\d+),'
                                r'(?P<Z>\d+\.\d+|-\d+\.\d+|\d+)?(?:,"(?P<Code>.*?)")?,?')

index_of_line = 0
dic_of_line_class = []

for line in file:
    if line_pattern.match(line):
        line_id = line_pattern.match(line).groupdict()
        line_points = generate_line_names_points()
        pp = pprint.PrettyPrinter(width=41, compact=True)

        #Tworzenie instancji klasy Line
        line_instance = Line(line_id, line_points)

        # Przypisanie instancji do słownika pod unikalnym kluczem
        dic_of_line_class.append(line_instance)
        index_of_line += 1

lvl_of_simplifier = 2
new_line = []
new_line_info = []
file_name = file.file_name.rstrip('.json') + "_new_lines.json"

for i in dic_of_line_class:
    i= i.line_class
    new_line = i['PointList'][0::lvl_of_simplifier]
    new_line_info.append({'Info': i['Info'], 'PointList': new_line})
    # File.json_file(new_line_info, file_name)
pp.pprint(new_line_info)