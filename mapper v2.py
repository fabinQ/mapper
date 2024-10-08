import os
import json
import datetime
import re


def create_subfolder(subfolder):
    # Funkcja sprawdza czy subfolder istnieje, jeśli nie to go tworzy
    if not os.path.exists(os.path.join('.', subfolder)):
        os.mkdir(subfolder)

def quote(argument):
    # Funkcja dodaje "" jeśli argument nie jest pusty - "argument"
    if argument.__class__ is dict:
        for key, value in argument.items():
            if not value is None:
                value = value.strip('"')
            argument.update({key: value})
        return argument
    elif argument:
        return f'"{argument}"'
    else:
        return ''

class Saver:
    # instancja klasy składająca się z klasy File i klas Line 
    def __init__(self, file_instance, lines_instance):
        self.File_instance = file_instance
        self.Lines = lines_instance

    def line(self):
        # Zwraca kolejne instancje klasy Line
        for line in self.Lines:
            yield line

    def file_name_finished_file(self):
        # Tworzy ścieżkę do pliku geo
        return os.path.join('.', 'geo_files', str(self.File_instance).rstrip('.geo') + '_3DG.geo')


    def header_to_geo(self):
        # Z klasy File tworzy nagłówek pliku geo
        # global header
        header = []
        for key, value in self.File_instance.get_header().items():
            if key == 'File':
                # pomija nazwe pliku
                pass
            elif key == 'Header':
                header = ['FileHeader ', ",".join(f'"{_}"'for _ in value), '\nbegin\n']
            else:
                header.append(f'\tFileInfo {quote(key)},{quote(value)}\n')
        header.extend(['end\n', 'PointList\n', 'LineList\n', 'begin\n'])
        return header

    def line_to_geo(self):
        # Z klasy Line tworzy linie do pliku geo
        lines = []
        # TODO poprawić tę funkcje - dodaje None
        for line in self.line():
            # Najpierw tworzy id linii
            id_line = line.get_line_id()
            lines.append(f'\tLine {quote(id_line["ID_line"])},{id_line["Polygon"]},{id_line["Descriptoin"]}')
            lines.extend(['\n\tbegin\n', '\t\tPointList\n', '\t\tbegin'])

            for point in line.get_point_list():
                # Potem dodaje współrzędne linii
                lines.append(
                    f'\n\t\tPoint {quote(point["Number"])},{point["X"]},{point["Y"]},{point["Z"]},{point["Code"]},,')

            lines.extend(
                ['\n\t\tend', '\n\t\tAttributeList', '\n\t\tbegin', '\n\t\t\tAttribute', '\n\t\tend', '\n\tend\n'])
        lines.extend(['end\n', 'AttributeList'])
        return lines

    def save_to_geo_file(self):
        # Tworzy subfolder, oraz zapisuje nagłówek i linie
        create_subfolder('geo_files')
        with open(self.file_name_finished_file(), "w", encoding="utf-8") as geo_file:
            geo_file.writelines(File.header_to_geo(self))
            geo_file.writelines(File.line_to_geo(self))


class File(Saver):
    # Tworzy instancje klasy File - jest jednocześnie generatorem. Tworzy nagłówek i zapisuje do pliku json
    def __init__(self, file_path):
        if not file_path.lower().endswith('.geo'):
            raise ValueError('Nieprawidłowe rozszerzenie pliku.')
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

    def header(self):
        # Utworzenie zmiennych składowych takich jak nazwa pliku
        file_info = {'File': File.__str__(self)}  #### self.__str__()

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

    def get_header(self):
        return self.file_info

    @staticmethod
    def json_file(content, file_name):
        # Sprawdza, czy dany katalog istnieje, jeśli nie to go tworzy
        create_subfolder('json')

        # Zapisuje do pliku
        with open(file_name, "a", encoding="utf-8", errors="xmlcharrefreplace") as json_file:
            json.dump(content, json_file, indent=2)
            json_file.write('\n')

    @property
    def formatted_datatime(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H.%M.%S")


class Line(Saver):

    def __init__(self, line_id_class, line_point_class):
        self.line_id_class = line_id_class
        self.line_point_class = line_point_class
        self.line_class = {'Line': ({'Info': self.line_id_class, 'PointList': self.line_point_class})}
        # self.json_file(self.line_class, file_name)

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
        list_of_line_class = []
        # Generowanie nowych instancji linii z pliku tekstowego
        for line in file:
            # Jeśli znajdzie pattern linii to odczytuje opis tej linii, następnie odczytuje punkty tej linii
            if line_pattern.match(line):
                line_id = quote(line_pattern.match(line).groupdict())
                line_points = Line.generate_line_points()

                # Tworzenie instancji klasy Line
                line_instance = Line(line_id, line_points)

                # Przypisanie instancji do słownika pod unikalnym kluczem
                list_of_line_class.append(line_instance)
        return list_of_line_class



# file = File('krawedzie.geo')
file = File('skarpy_EdgeLines.geo')
# file = File('GRZ-25511-27300.geo')
# file = File('krawedzie3.geo')
# file = File('1.geo')
# file = File('Chorzew_T5_spód_tłucznia.geo')
# file = File('Chorzew_T5_spód_tłucznia v2.geo')
# file = File('lk zegrze.geo')
# file = File('ŚR i CH.geo')

assert str(file).endswith('.geo')

line_pattern = re.compile(r'\tLine (?P<ID_line>.+?)?,(?P<Polygon>\d+|)?,(?P<Descriptoin>.+)?')
line_point_pattern = re.compile(r'\t\t\tPoint(?P<Number>.+?)?,(?P<X>\d+\.\d+|\d+),(?P<Y>\d+\.\d+|\d+),'
                                r'(?P<Z>\d+\.\d+|-\d+\.\d+|\d+)?(?:,"(?P<Code>.*?)")?,?')


# Generowanie nowych instancji linii z pliku tekstowego
list_of_line_class = Line.generate_line_names()

# Utworzenie nowego pliku z liniami (opcja)
# file_name = file.file_name.rstrip('.json') + "_new_lines.json"

# Utworzenie zmiennej do upraszczania oraz utworzenie listy klas linii po wyprostowaniu
level_of_simplify = 5
list_of_line_class = Line.simplifier(list_of_line_class, level_of_simplify)

SaverInstance = Saver(file, list_of_line_class)
SaverInstance.save_to_geo_file()
