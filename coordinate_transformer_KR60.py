# -*- coding: utf-8 -*-

import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# --- Konfiguracja ---
# Nazwa pliku wejściowego z danymi w układzie PL-2000 i wysokościami Kronsztadt 86.
# Format pliku: [NumerPunktu X Y H86] oddzielone spacjami lub tabulatorami.

def plik_wejsciowy_exists():
    try:
        PLIK_WEJSCIOWY = input("Podaj ścieżke do pliku .txt z punktami [PKT X Y Z]\n")
        # Sprawdzenie, czy plik istnieje
        if not os.path.exists(PLIK_WEJSCIOWY):
            PLIK_WEJSCIOWY = PLIK_WEJSCIOWY.strip('"')
        if not os.path.exists(PLIK_WEJSCIOWY):
            raise FileNotFoundError(f"Plik '{PLIK_WEJSCIOWY}' nie istnieje.")
        
    except FileNotFoundError as e:
        print(f"BŁĄD: {e}")
        print("Proszę podać poprawną ścieżkę do pliku.")
        return plik_wejsciowy_exists()
    return PLIK_WEJSCIOWY



# --- Model przeliczenia ---
# Różnica wysokości między układem Kronsztadt 86 a Kronsztadt 60 nie jest stała.
# Zmienia się ona od ok. 0.14m na południu do ok. 0.26m na północy Polski.
# H_Kronsztadt60 = H_Kronsztadt86 - delta
# Poniżej zastosowano średnią wartość dla Polski, wynoszącą około 0.17 metra.
# Możesz dostosować tę wartość, jeśli znasz bardziej precyzyjną poprawkę dla swojego regionu.

def srednia_poprawka_metry():
    """
    Funkcja zwraca średnią poprawkę wysokości z Kronsztadt 86 na Kronsztadt 60.
    Wartość ta jest używana do przeliczenia wysokości w pliku wejściowym.
    """
        # Uruchom funkcję pokaz_obraz_poprawek() w osobnym wątku
    pokaz_obraz_poprawek()
    SREDNIA_POPRAWKA_METRY = input("Podaj wartość średniej poprawki (H86 - H60) w metrach: ")
    try:
        SREDNIA_POPRAWKA_METRY = float(SREDNIA_POPRAWKA_METRY)
    except ValueError:
        print("BŁĄD: Wprowadź liczbę zmiennoprzecinkową.")
        return srednia_poprawka_metry()
    if SREDNIA_POPRAWKA_METRY > 0.14 or SREDNIA_POPRAWKA_METRY < -0.0123:
        print("BŁĄD: Wartość poprawki musi być w zakresie od 0.14 do -0.0123 metra.")
        return srednia_poprawka_metry()
    return SREDNIA_POPRAWKA_METRY


def pokaz_obraz_poprawek():
    """
    Funkcja otwiera i wyświetla plik .jpg, który może pomóc w określeniu współczynnika średnia_poprawka_metry.
    """
    nazwa_pliku = 'przeliczanie_KR86_KR6010.png'
    if not os.path.exists(nazwa_pliku):
        print(f"BŁĄD: Plik '{nazwa_pliku}' nie został znaleziony.")
        return
    
    # Utwórz nowe okno matplotlib
    fig, ax = plt.subplots()
    img = mpimg.imread(nazwa_pliku)
    ax.imshow(img)
    ax.axis('off')
    ax.set_title(f"Podgląd pliku: {nazwa_pliku}")
    
    # Wyświetl w trybie nieblokującym
    plt.show(block=False)
    plt.draw()  # Wymuś odświeżenie okna
    


def przelicz_wysokosci():
    """
    Główna funkcja skryptu. Wczytuje dane z pliku wejściowego, przelicza
    wysokości z Kronsztadt 86 na Kronsztadt 60 i zapisuje wyniki do pliku wyjściowego.
    """
    print("--- Start programu ---")
    
    
    licznik_linii = 0
    licznik_sukcesow = 0
    licznik_bledow = 0

    print(f"Wczytuję plik: '{PLIK_WEJSCIOWY}'")
    print(f"Zastosowana poprawka (H86 - H60): {SREDNIA_POPRAWKA_METRY:.3f} m")
    
    try:
        # Otwarcie pliku wejściowego do odczytu i wyjściowego do zapisu
        with open(PLIK_WEJSCIOWY, 'r', encoding='utf-8') as plik_in, \
             open(PLIK_WYJSCIOWY, 'w', encoding='utf-8') as plik_out:
            
            # Przetwarzanie każdej linii w pliku
            for linia in plik_in:
                licznik_linii += 1
                
                # Pomiń puste linie i linie komentarza
                if not linia.strip() or linia.strip().startswith('#'):
                    continue

                # Podziel linię na części (numer, X, Y, H)
                czesci = linia.split()

                if len(czesci) != 4:
                    print(f"BŁĄD w linii {licznik_linii}: Nieprawidłowa liczba kolumn. Oczekiwano 4, otrzymano {len(czesci)}. Linia: '{linia.strip()}'")
                    licznik_bledow += 1
                    continue
                
                numer_punktu = czesci[0]
                
                try:
                    # Konwersja współrzędnych i wysokości na liczby
                    x = float(czesci[1])
                    y = float(czesci[2])
                    h86 = float(czesci[3])
                    
                    # Obliczenie nowej wysokości
                    h60 = h86 + SREDNIA_POPRAWKA_METRY
                    # Zapisanie wyniku do pliku wyjściowego w formacie: NumerPunktu X Y Z (oddzielone spacjami)
                    plik_out.write(f"{numer_punktu} {x} {y} {h60}\n")
                    licznik_sukcesow += 1

                except ValueError:
                    print(f"BŁĄD w linii {licznik_linii}: Nie można przekonwertować współrzędnych na liczby. Linia: '{linia.strip()}'")
                    licznik_bledow += 1
                    continue
    
    except IOError as e:
        print(f"BŁĄD: Wystąpił problem z odczytem lub zapisem pliku: {e}")
        return

    print("\n--- Zakończono przetwarzanie ---")
    print(f"Przetworzono linii: {licznik_linii}")
    print(f"Zapisano punktów: {licznik_sukcesow}")
    print(f"Pominięto z powodu błędów: {licznik_bledow}")
    print(f"Wyniki zostały zapisane w pliku: '{PLIK_WYJSCIOWY}'")


def main():
    """
    Główna funkcja programu, która uruchamia proces przeliczania wysokości.
    """
    print("Uruchamianie programu przeliczania wysokości z Kronsztadt 86 na Kronsztadt 60...")
    PLIK_WEJSCIOWY = plik_wejsciowy_exists()

    # Nazwa pliku, w którym zostaną zapisane wyniki.
    PLIK_WYJSCIOWY = PLIK_WEJSCIOWY.replace('.txt', '_KR60.txt')

    SREDNIA_POPRAWKA_METRY = srednia_poprawka_metry()
    przelicz_wysokosci()
    print("Program zakończył działanie.")
if __name__ == '__main__':
    main()
