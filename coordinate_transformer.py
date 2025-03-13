import os

import pyproj

# Lista współrzędnych geocentrycznych (X, Y, Z)
print("Podaj ścieżke do pliku")
path= input().strip('"')
station = []
new_line = []
with open(path, "r", encoding="UTF8") as file:
    stations = []
    for line in file:
        new_line = []
        line = line.split("\t")
        for x in line:
            x = x.replace("\n", "")
            x = x.replace(" ", "")
            x = x.replace(",", ".")

            new_line.append(x)
        stations.append(new_line)

stations_dic = {}
for station in stations:
    krotka = (float(station[1]), float(station[2]), float(station[3]))
    stations_dic[station[0]]=krotka


# Definicja układów współrzędnych
geocentric = pyproj.CRS("EPSG:4978")  # WGS84 geocentryczny
pl92 = pyproj.CRS("EPSG:2180")  # Układ PL-1992

# Transformator
transformer = pyproj.Transformer.from_crs(geocentric, pl92, always_xy=True)

# Konwersja współrzędnych
converted_stations = {}
for name, (X, Y, Z) in stations_dic.items():
    easting, northing, height = transformer.transform(X, Y, Z)
    converted_stations[name] = (easting, northing)
    print(f"{name}: {northing:.3f}, {easting:.3f}")
