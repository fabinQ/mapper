import os
import pyperclip
import itertools as it
# import glob

def scantree(path):
    for i in os.scandir(path):
        if i.is_file():
            yield i



path = input("Podaj ścieżke mordo ")
print(path)
extension_lin = '.lin'
extension_trm = '.trm'

# # a = glob.glob(path+'\\*'+extension_lin)
# # print(list(os.path.basename(i) for i in a))
# # for i in a:
# #     print(os.path.basename(i))
#
# files = []
# for filename_with_excetion in os.listdir(path):
#     filename, extension = os.path.splitext(filename_with_excetion)
#     if extension == extension_lin or extension == '.l3d':
#         print("Oś: ", filename)
#         files.append(filename_with_excetion)
#     elif extension == extension_trm:
#         print("Model: ",filename)
#         files.append(filename_with_excetion)
#
# print('\nW katalogu jest {} plików.'.format(len(files)))
# pyperclip.copy('\n'.join(files))

print(''*2)
files = []
for i in scantree(path):
    files.append(i.name)

files = sorted(files, key= lambda x: os.path.splitext(x))
sum_of_files = 0
for excention, file in it.groupby(files,key= lambda x: os.path.splitext(x)[1]):
    file = list(file)
    sum_of_files+=len(file)
    print('{} = {}'.format(excention, len(list(file))))
print('Całkowita ilość plików to: ', sum_of_files,'\n')
for i in files:
    print('Model: {}'.format(i) if os.path.splitext(i)[1] == extension_trm else 'Oś: {}'.format(i))
pyperclip.copy('\n'.join(files))
