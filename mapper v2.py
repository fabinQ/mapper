import os

#definicja pliku
file = 'krawedzie.geo'

#Otwarcie pliku
file = open(file,'r')

#Generator linii
def file_line_generator(file):
    for line in file:
        line = line.strip()
        yield line

for line in file_line_generator(file):
    print(line)
class File:
    def __init__(self, header, info_list):
        self.header = header
        self.info_list = info_list

    def __str__(self):
        header_str = f"FileHeader {self.header[0]}, {self.header[1]}, {self.header[2]}"
        info_str = "\n".join([f'FileInfo "{key}","{value}"' for key, value in self.info_list.items()])
        return f"{header_str}\n{info_str}"
