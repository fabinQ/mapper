import os


class File:
    def __init__(self, file_path):
        self.file_path = open(file_path, 'r')
        self.file_info = self.header()

    def __next__(self):
        return next(self.file_path).strip()
    def __iter__(self):
        return self


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


# for line in file:
#     print(line)


class FileLine(File):
    def __init__(self, file_path, file_info):
        File.__init__(file_path,file_info)
        self.version_SBG = file_info[0][0]
        self.type_document = file_info[0][1]
        self.coding = file_info[0][3]
        self.application = file_info[1][1]
        self.serialNo =file_info[2][1]
        self.author = file_info[3][1]
        self.company = file_info[4][1]
        self.description = file_info[5][0]
        self.coordinate_system = file_info[6][0]
    def __str__(self):
        print(f"{self.version_SBG}-{self.type_document}-{self.coding}-{self.application} - {self.serialNo} - {self.author} - {self.company} - {self.description} - {self.coordinate_system}")
        return f"{self.version_SBG}-{self.type_document}-{self.coding}-{self.application} - {self.serialNo} - {self.author} - {self.company} - {self.description} - {self.coordinate_system}"


print(str(FileLine))