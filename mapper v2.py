import os
import json
import sys


class File:
    def __init__(self, file_path):
        self.file_path = open(file_path, 'r')
        self.file_info = self.header()
        
    def __next__(self):
        return next(self.file_path).strip()

    def __iter__(self):
        return self

    def __str__(self):
        return '\n'.join((' - '.join(map(str, line)) for line in self.file_info))

    def header(self):
        file_info = []
        header_line = tuple(next(self.file_path).split('"')[1::2])
        file_info.append({'Header': header_line})
        next(self.file_path)
        while header_line != 'end':
            header_line = next(self.file_path).split('"')[1::2]
            if not header_line: break
            key = header_line[0]
            value = header_line[1] if len(header_line) > 1 else None
            file_info.append({key: value})

        print(file_info)
        return file_info

    def json_file(self):
        pass


file = File('krawedzie.geo')
print(str(file))

# for line in file:
#     print(line)
