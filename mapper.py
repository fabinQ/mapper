import os
import re
import numpy as np
from datetime import datetime
datetime_start = datetime.now()

path = os.getcwd()
plik = "Krawedzie3.geo"
# plik = "Krawędzie S7 -13 odl śred 0.05m min dlug linii 30m min rozm trójk 50m.geo"
path = os.path.join(path, plik)



# funkcja zwracająca pozycje linii, ich identyfikatory oraz kolory
def positon(path):
    with open(path, 'r') as f:
        lines = f.readlines()    # odczytanie wszystkich linii pliku
        num_lines = len(lines)
        poz = []
        id_line = []
        id_color = []
        for i, line in enumerate(lines, start=1):
            # print(i,line)
            match = re.search(r'Line "(\w+|\d+|\w+\d+\.\d+|\d+\.\d+\w+)"', line)  # wyszukanie identyfikatora linii
            match_color = re.search(r'Attribute "COLOR","(\d+)"', line)  # wyszukanie koloru linii
            if match != None:
                poz.append(i)  # dodanie pozycji linii do listy pozycji
                # print(f"Numer  linii: {match.group(1)}, Linia: {i}")
                id_line.append(match.group(1))  # dodanie identyfikatora linii do listy identyfikatorów
            if match_color != None:
                # print(f"Kolor  linii: {match_color.group(1)} Linia: {i}")
                id_color.append(match_color.group(1))
        poz.append(num_lines-1)  # dodanie końcowej pozycji pliku do listy pozycji
    return poz, id_line, id_color


# funkcja zwracająca rzeczywiste pozycje linii w pliku (bez nagłówków i metadanych)
def position_real(poz):
    poz = list(zip(poz, poz[1:]))
    poz_real = [(a+3, b-8) for a, b in poz]  # rzeczywiste pozycje linii w pliku
    return poz_real


# funkcja zwracająca współrzędne punktów
def points_finder(path, poz_real):
    with open(path, 'r') as f:
        lines = f.readlines()
    data = []
    for start, end in poz_real:
        fragment = ''.join(lines[start:end+1])  # odczytanie fragmentu pliku od-do linii
        match = re.findall(r'Point ,([\d\.e+-]+)\s?,([\d\.e+-]+)\s?,([\d\.e+-]+),', fragment)  # wyszukanie współrzędnych punktów
        data.append(match)

    # konwersja współrzędnych na typ float
    data_float = []
    for lst in data:
        lst_float = []
        for tpl in lst:
            tpl_float = tuple(float(x) for x in tpl)
            lst_float.append(tpl_float)
        data_float.append(lst_float)
    return data_float

def printuj(id_line, id_color, data_float):
    data_global = list(zip(id_line,  id_color, data_float))
    for i in data_global:
        print("Linia o ID {} i kolorze {} składa się z {} puntów".format(i[0], i[1], len(i[2])))
        print("Te punkty to: ")
        for x in i[2]:
            print(x)
        print()
def printuj_2(*args):
    for i in args:
        for l in i:
            print(l)

def points_id(data_float):
    #najpierw przypisać lp do data_float
    lp = []
    for i in data_float:
        lp.append(list(range(0,len(i))))
        print('Uwaga len data float {}, lp {}'.format(len(i),list(range(0,len(i)))))
    data_id = [list(zip(sublist1, sublist2)) for sublist1, sublist2 in zip(lp, data_float)]
    for i in data_id:
        print(i)
    print('$'*50+'\n')
    return data_id

def azimuth(data_id):
    tab_of_azimuth = []
    delta_xX = []
    delta_yY = []

    for line in data_id:
        delta_x = []
        delta_y = []
        for i in range(1, len(line)):
            # print("Odejmuje {} od {} = {}".format(line[i][1][0], line[i-1][1][0], line[i][1][0] - line[i-1][1][0]))
            delta_x.append(line[i][1][0] - line[i-1][1][0])
            delta_y.append(line[i][1][1] - line[i-1][1][1])
        delta_xX.append(delta_x)
        delta_yY.append(delta_y)
    #Wyświetlanie delt
    # for n,m in zip(delta_xX,delta_yY):
    #     print("Delta X ", n)
    #     print("Delta Y ", m)
    # print('*'*30 )

    delta_XY = [list(zip(sublist1, sublist2)) for sublist1, sublist2 in zip(delta_xX, delta_yY)]
    for i in delta_XY:
        # print(i)
        azimuth_line = []
        for p in i:
            # print()
            # print(p)
            # Liczy azymut
            try:
                fi = np.arctan(p[1]/p[0])
            except:
                if p[1]==0:
                    fi = 0.0
                    print('Duplikat - Pierwsza ćwiartka')
                if p[1]>0:
                    fi = 100.0
                    print('Dx = 0 Pierwsza ćwiartka')
                if p[1]<0:
                    fi = 300.0
                    print('Dx = 0 Trzecia ćwiartka')
                azimuth_line.append(fi)
                print(azimuth_line[-1])
                continue

            fi = (200/np.pi)*fi
            # print("Fi", fi)
            # Sprawdza ćwiartki
            # Pierwsza ćwiartka
            if p[0] >=0 and p[1] >=0:
                fi = fi
                # print('Pierwsza ćwiartka')
            # Druga lub trzecia ćwiartka
            if p[0] < 0:
                fi = fi + 200
                # print('Druga lub trzecia ćwiartka')
            # Czwarta ćwiartka
            if p[0] >= 0 and p[1] < 0:
                fi = fi + 400
                # print('Czwarta ćwiartka')
            azimuth_line.append(fi)
            # print(azimuth_line[-1])
        tab_of_azimuth.append(azimuth_line)
        # print(tab_of_azimuth)
    # Wyświetlanie max
    # a= (list(max(i) for i  in tab_of_azimuth))
    # print(a)
    # print(max(a))
    return tab_of_azimuth

def median_mean(*args):
    tab_of_sub_lines =[]
    for lines in args:
        for line in lines:
            i = 0
            print('Linia')
            print(line)
            while i < len(line):
                # print('zaczynam')
                if i+10<len(line):
                    sub_line = line[i:i+5]
                else:
                    # print('tu')
                    sub_line = line[i:]
                    i+= len(line)%5
                # print(i, i+5)
                # print(len(line))
                # print(sub_line)
                tab_of_sub_lines.append(sub_line)
                # print(tab_of_sub_lines)
                i+=5
    for i in tab_of_sub_lines:
        print("tab_of_sub_lines")
        print(i)
        mean_value = np.mean(sub_line)
        median_value = np.median(sub_line)
        print(
            'Średnia sublisty z {} elementami to {}, a mediana to {} różnica między nimi wynosi {}. Wartość max {} a min {}'.format(
                len(sub_line), mean_value, median_value, abs(mean_value - median_value),
                median_value + abs(mean_value - median_value), median_value - abs(mean_value - median_value)))
        for i in sub_line:
            if i >= median_value + abs(mean_value - median_value):
                print(i)
            if i <= median_value - abs(mean_value - median_value):
                print(i)


poz, id_line, id_color = positon(path)
poz_real = position_real(poz)
data_float = points_finder(path, poz_real)
# printuj(id_line, id_color, data_float)
data_id = points_id(data_float)
tab_of_azimuth = azimuth(data_id)
# printuj_2(tab_of_azimuth)
data_id = points_id(tab_of_azimuth)
print(data_id)
# printuj_2(data_id)
median_mean(tab_of_azimuth)

datetime_stop = datetime.now()
print("Czas wykonania to {} sekund.".format(datetime_stop-datetime_start))
