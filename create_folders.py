import os


folders = folders.split("\n")
print(folders)
for folder in folders:
    print(folder)
    pathFolder = os.path.join(path, folder)
    os.mkdir(pathFolder)

def main():
    path = input("Podaj ścieżke mordo\n")
    path = "C:\Users\Hyperbook\Desktop\Nowy folder"
    folders = input("Podaj nazwy folderów\n")
    folders = "GEO WLOKNINY 136,19\nGEO WLOKNINY 136,19 - Tri\nGEO WLOKNINY 136,64\nGEO WLOKNINY 136,69\nGEO WLOKNINY 137,14\nGEO WLOKNINY 137,19\nGEO WLOKNINY 137,64\nGEO WLOKNINY 137,84\nGEO WLOKNINY 138,10"

if __name__ == "__main__":
    main()
