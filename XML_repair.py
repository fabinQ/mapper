import xml.etree.ElementTree as ET


def remove_crosssects(file_path: str):
    try:
        # Wczytanie pliku XML z przestrzeniami nazw
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Przestrzeń nazw LandXML
        namespace = "http://www.landxml.org/schema/LandXML-1.2"
        ns = {'landxml': namespace}

        # Rejestracja domyślnej przestrzeni nazw
        ET.register_namespace("", namespace)

        # Znalezienie i usunięcie tagu CrossSects
        for parent in root.findall('.//landxml:Alignment', ns):
            for crosssects in parent.findall('landxml:CrossSects', ns):
                parent.remove(crosssects)

        # Nadpisanie pliku
        tree.write(file_path, encoding="utf-8", xml_declaration=True)
        print("Tag <CrossSects> został usunięty i plik został nadpisany.")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")

def main():
    print("Podaj ścieżke do pliku")
    file_path = input().strip('"')
    file_path.split('"')

    remove_crosssects(file_path)

if __name__ == "__main__":
    main()