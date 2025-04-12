import os
import pyperclip
import itertools as it
# import glob

def scantree(path):
    for i in os.scandir(path):
        if i.is_file():
            yield i




def main():

    # path = input("Podaj ścieżke mordo ")
    path = r"C:\OneDrive - 3D GEOSYSTEMY MICHAŁ JAŚKIEWICZ\Projekty iCON Office\LEWCZUK\LK 201\Korytarze\17.01.2025"
    print(path)
    extensionTrm = '.trm'
    files = []

    for i in scantree(path):
        files.append(i.name)

    files = sorted(files, key= lambda x: os.path.splitext(x))

    sunOfFile = 0
    dicOfExtension = dict()
    for excentionOfFile, typeOfExtension in it.groupby(files,key= lambda x: os.path.splitext(x)[1]):
        typeOfExtension = list(typeOfExtension)
        sunOfFile+=len(typeOfExtension)
        
        if excentionOfFile in dicOfExtension:
            dicOfExtension[excentionOfFile] += len(typeOfExtension)
        else:
            dicOfExtension[excentionOfFile] = len(typeOfExtension)

    print('Całkowita ilość plików to: ', sunOfFile,'\n')

    for file in files:
        print('{}'.format(file))

    for key, value in dicOfExtension.items():
        print(f"{key} = {value}")
    pyperclip.copy('\n'.join(files))

if __name__ == "__main__":
    main()