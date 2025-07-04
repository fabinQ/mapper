import os

def createFilders(folders,path):
    folders = folders.split("\n")
    print(folders)
    for folder in folders:
        print(folder)
        pathFolder = os.path.join(path, os.path.splitext(folder)[0])
        os.mkdir(pathFolder)

def main():
    # path = input("Podaj ścieżke mordo\n")
    path = "C:\OneDrive - 3D GEOSYSTEMY MICHAŁ JAŚKIEWICZ\Projekty iCON Office\KB CONSTRUCTION\OSTRODA\Trimble\ostroda"
    # folders = input("Podaj nazwy folderów\n")
    folders = "Tor 2 Dół warstwy ochronnej 257+859-260+350.trm\nTor 2 Góra warstwy ochronnej 257+859-260+350.trm\nTor4 dół klińca 258+043-259+431.trm\nTor4 góra klińca 258+043-259+431.trm"
    createFilders(folders,path)
if __name__ == "__main__":
    main()
