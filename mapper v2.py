import os
import json
import sys
import datetime
import re
from abc import ABC, abstractmethod


class Saver():
    def __init__(self, File_instance, Lines):
        self.File_instance = File_instance
        self.Lines = Lines

    def line(self):
        for line in self.Lines:
            yield line

    def file_name_finished_file(self):
        return os.path.join('.','geo_files', str(self.File_instance).rstrip('.geo') + '_3DG.geo')


    def create_subfolder(self, subfolder):
        if not os.path.exists(os.path.join('.',subfolder)):
            os.mkdir(subfolder)

    def header_to_geo(self):
        header = ['FileHeader ',",".join(f'"{value}"' for value in self.File_instance.get_header()['Header']), '\nbegin']
        file_info = ['\tFileInfo '.join(f'"{value}"' for value in self.File_instance.get_header()['Header'])]
        return header

    def save_to_geo_file(self):
        self.create_subfolder('geo_files')
        print(self.header_to_geo())
        print(self.file_name_finished_file())
        with open(self.file_name_finished_file(), "w", encoding="utf-8") as geo_file:
            geo_file.writelines(File.header_to_geo(self))
            # while self.line():
            #     print(self.line())


class File(Saver):
    # TODO: Sprawdzić hierarchię klas
    def __init__(self, file_path):
        self.data_time_stamp = self.formatted_datatime
        self.file_path = open(file_path, 'r', encoding='utf-8')
        self.file_info = self.header()
        self.file_name = './json/' + self.data_time_stamp + ' ' + self.file_info.get('Company') + '.json'
        self.json_file(self.file_info, self.file_name)

    def __next__(self):
        return next(self.file_path).rstrip()

    def __iter__(self):
        return self

    def __str__(self):
        return self.file_path.name
    # TODO: ewentualnie dodać __enter__ __exit__

    # TODO: Dodać funkcję zapisywania pliku .geo - nagłówek + linie

    def header(self):
        # Utworzenie zmiennych składowych takich jak nazwa pliku
        file_info = {'File': File.__str__(self)}

        # Nagłówek Header
        header_line = tuple(next(self.file_path).split('"')[1::2])
        file_info.update({'Header': header_line})

        # Reszta file info przystosowanym do formatu pliku.
        next(self)
        header_line = next(self.file_path).split('"')[1::2]

        while header_line:
            key = header_line[0]
            value = header_line[1] if len(header_line) > 1 else None
            file_info.update({key: value})
            header_line = next(self.file_path).split('"')[1::2]
        print(file_info)
        return file_info

    def json_file(self, content, file_name):

        # Sprawdza, czy dany katalog istnieje, jeśli nie to go tworzy
        self.create_subfolder('json')

        # Zapisuje do pliku
        with open(file_name, "a", encoding="utf-8", errors="xmlcharrefreplace") as json_file:
            json.dump(content, json_file, indent=2)
            json_file.write('\n')


    def get_header(self):
        return self.file_info
    @property
    def formatted_datatime(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H.%M.%S")


class Line(Saver):
    def __init__(self, line_id_class, line_point_class):
        self.line_id_class = line_id_class
        self.line_point_class = line_point_class
        self.line_class = {'Line': ({'Info': self.line_id_class, 'PointList': self.line_point_class})}
        # self.json_file(self.line_class, file_name)
        # number_of_line +=1

    def __str__(self):
        return str(self.line_class)

    def get_line_class(self):
        return self.line_class

    def get_line_id(self):
        return self.line_id_class

    def get_point_list(self):
        return self.line_point_class




    @staticmethod
    def simplifier(list_of_line_class, level_of_simplify):
        for current_line in list_of_line_class:
            current_point_line = current_line.line_point_class[0::level_of_simplify]
            current_line.line_class.update(
                {'Line': {'Info': current_line.line_class['Line']['Info'], 'PointList': current_point_line}})
        return list_of_line_class

    @staticmethod
    def generate_line_points():

        # Generowanie punktów linii.
        line_point = []
        for _ in file:
            if line_point_pattern.match(_):
                line_point_dic = line_point_pattern.match(_).groupdict()
                line_point.append(line_point_dic)
            elif _ == '\tend':
                return line_point

    @staticmethod
    def generate_line_names():
        # Generowanie nowych instancji linii z pliku tekstowego
        for line in file:
            # Jeśli znajdzie pattern linii to odczytuje opis tej linii, następnie odczytuje punkty tej linii
            if line_pattern.match(line):
                line_id = line_pattern.match(line).groupdict()
                line_points = Line.generate_line_points()

                # Tworzenie instancji klasy Line
                line_instance = Line(line_id, line_points)

                # Przypisanie instancji do słownika pod unikalnym kluczem
                list_of_line_class.append(line_instance)
        return list_of_line_class

# class Abstract(File):
#     def __init__(self, list):
#         self.list = list
#         self.file_path = './geo_files/' + File.__str__(file).rstrip('.geo') + '_3DG.geo'
#

#     @abstractmethod
#     def __str__(self):
#         pass
#     def get_header(self):
#         super().get_header()


# file = File('krawedzie.geo')
file = File('GRZ-25511-27300.geo')
# file = File('krawedzie3.geo')
# file = File('1.geo')
# file = File('Chorzew_T5_spód_tłucznia.geo')
# file = File('Chorzew_T5_spód_tłucznia v2.geo')
# file = File('lk zegrze.geo')
# file = File('ŚR i CH.geo')

assert str(file).endswith('.geo')

line_pattern = re.compile(r'\tLine "(?P<ID_line>.+?)"?,(?P<Polygon>\d+|)?,(?P<Descriptoin>.+)?')
line_point_pattern = re.compile(r'\t\t\tPoint(?: "(?P<Number>.+|)")?,(?P<X>\d+\.\d+|\d+),(?P<Y>\d+\.\d+|\d+),'
                                r'(?P<Z>\d+\.\d+|-\d+\.\d+|\d+)?(?:,"(?P<Code>.*?)")?,?')

list_of_line_class = []

# Generowanie nowych instancji linii z pliku tekstowego
list_of_line_class = Line.generate_line_names()

# Utworzenie nowego pliku z liniami (opcja)
# file_name = file.file_name.rstrip('.json') + "_new_lines.json"

# Utworzenie zmiennej do upraszczania oraz utworzenie listy klas linii po wyprostowaniu
level_of_simplify = 5
list_of_line_class = Line.simplifier(list_of_line_class, level_of_simplify)

SaverInstance = Saver(file, list_of_line_class)
SaverInstance.save_to_geo_file()

# TODO: sprawdzić co tu się dzieje
# y = {}
# for x in list_of_simplifier_line_class:
#     print(x)
    # print(x.get_line_class())
    # print(x.get_point_list())
    # print(x.get_line_id())
    # y = {x.get_line_id(): x.get_point_list()}
    # print(y)
    # y.append(list(x))
# print(y)
