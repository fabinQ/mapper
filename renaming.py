from urllib.parse import unquote

import os.path

def patch_creator( catalog, file):
    return os.path.join(catalog,file)
def get_files(current_path, extension, recursive = False):
    fitFiles = []

    if (os.path.exists(current_path)):
        if recursive:
            for catalog, _, files in os.walk(current_path):
                for file in files:
                    if file.endswith(extension):
                        fitFiles.append(patch_creator(catalog, file))
        else:
            for fileString in os.listdir(current_path):
                file = patch_creator(current_path, fileString)
                if os.path.isfile(file) and fileString.endswith(extension):
                    fitFiles.append(file)
    return fitFiles

def rename_file( files ):
    for file in files:
        catalog, fileName = os.path.split(file)
        newFileName = unquote(fileName)
        newFilePath = patch_creator(catalog, newFileName)

        if newFileName != fileName:
            os.rename(file, newFilePath)


def main():
    print("Podaj ścieżkę: ")
    current_path = input()
    extension = ".xml"

    fitFiles = get_files(current_path, extension, recursive = True)
    rename_file(fitFiles)

if __name__ == "__main__":
    main()