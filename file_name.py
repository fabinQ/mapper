import os
import pyperclip
import itertools as it


def scantree(path):
    for i in os.scandir(path):
        if i.is_file():
            yield i

def sumAndListOfFileInDictionary(dicOfExtension):
    sumOfFile = 0
    listOfExtensionSum = []
    listOfFiles = []

    for extension, extensionFileList in dicOfExtension.items():
        lenOfFilesWithExtension = len(extensionFileList)

        sumOfFile += lenOfFilesWithExtension
        listOfExtensionSum.append((extension, lenOfFilesWithExtension))

        listOfFiles.extend(extensionFileList)

        print(f"Pliki z rozszerzeniem '{extension}':")
        for file in extensionFileList:
            print(f"  {file}")

    print('\nCałkowita ilość plików to: ', sumOfFile)
    print('Lista plików z rozszerzeniem:')
    for extension, count in listOfExtensionSum:
        print(f"    {extension} = {count}")
    pyperclip.copy('\n'.join(listOfFiles))



def selectFiles(path, *extensions):
    files = []
    for file in scantree(path):
        if not extensions or file.name.endswith(extensions):
                files.append(file.name)
    return files

def groupByExtension(path, *extensions):
    dicOfExtension = dict()

    for file in scantree(path):
        if not extensions or file.name.endswith(extensions):
            extension = os.path.splitext(file.name)[1]
            if extension not in dicOfExtension:
                dicOfExtension[extension] = []
            dicOfExtension[extension].append(file.name)
           
    return dicOfExtension


def main():

    path = input("Podaj ścieżke mordo ")
    # path = r"C:\OneDrive - 3D GEOSYSTEMY MICHAŁ JAŚKIEWICZ\Projekty iCON Office\KB CONSTRUCTION\OSTRODA\PODFOLDERY\14.04.2025"
    print(path)
    extensionTrm = '.trm'
    extensionL3d = '.l3d'
    extensionXML = '.xml'
    extensionTxt = '.txt'


    dicOfExtension = groupByExtension(path, extensionTrm, extensionL3d,extensionXML,extensionTxt)
    sumAndListOfFileInDictionary(dicOfExtension)



if __name__ == "__main__":
    main()