import os


class File:
    def __init__(self, file_path):
        self.file_path = open(file_path, 'r')
        self.file_info = self.header()


    def __next__(self):
        return next(self.file_path).strip()
    def __iter__(self):
        return self

    def __str__(self):
        return '\n'.join([' - '.join(map(str, line)) for line in self.file_info])


    def header(self):
        file_info = []
        header_line = next(self.file_path).split('"')[1::2]
        file_info.append(header_line)
        next(self.file_path)
        while header_line:
            header_line = next(self.file_path).split('"')[1::2]
            file_info.append(header_line)
        file_info.pop()
        print(file_info)
        return file_info

file = File('krawedzie.geo')
print(str(file))

# for line in file:
#     print(line)