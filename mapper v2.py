import os


class File:
    def __init__(self, file_path):
        self.file_path = open(file_path, 'r')

    def __next__(self):
        self.file_handle = next(self.file_path).strip()
        return self.file_handle
    def __iter__(self):
        return self


file = File('krawedzie.geo')


for line in file:
    print(line)


class FileLine(File):
    def __init__(self, header, info_list):
        self.header = header
        self.info_list = info_list

    def __str__(self):
        header_str = f"FileHeader {self.header[0]}, {self.header[1]}, {self.header[2]}"
        info_str = "\n".join([f'FileInfo "{key}","{value}"' for key, value in self.info_list.items()])
        return f"{header_str}\n{info_str}"

