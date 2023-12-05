import os


class File:
    def __init__(self, file_path):
        self.file_path = open(file_path, 'r')
        self.file_info = self.header()
        self.version_SBG = self.file_info[0][0]
        self.type_document = self.file_info[0][1]
        self.coding = self.file_info[0][2]
        self.application = self.file_info[1][1]
        self.serialNo = self.file_info[2][1]
        self.author = self.file_info[3][1]
        self.company = self.file_info[4][1]
        self.description = self.file_info[5][0]
        self.coordinate_system = self.file_info[6][0]

    def __next__(self):
        return next(self.file_path).strip()
    def __iter__(self):
        return self

    def __str__(self):
        return f"{self.version_SBG}-{self.type_document}-{self.coding}-{self.application} - {self.serialNo} - {self.author} - {self.company} - {self.description} - {self.coordinate_system}"


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