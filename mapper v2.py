import os

class File:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_handle = None
    def __next__(self):
        if self.file_handle is None:
            self.file_handle = open(self.file_path, 'r')

        line = next(self.file_handle, None)
        if line is None:
            # Zamknij plik, gdy osiągniemy koniec
            self.file_handle.close()
            raise StopIteration
        return line.rstrip()

    def __iter__(self):
        return self

file = File('krawedzie.geo')



for line in file:
    print(line)

class File_line(File):
    def __init__(self, header, info_list):
        self.header = header
        self.info_list = info_list

    def __str__(self):
        header_str = f"FileHeader {self.header[0]}, {self.header[1]}, {self.header[2]}"
        info_str = "\n".join([f'FileInfo "{key}","{value}"' for key, value in self.info_list.items()])
        return f"{header_str}\n{info_str}"
