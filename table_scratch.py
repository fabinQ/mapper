import requests
from bs4 import BeautifulSoup

def main():
    # URL strony do pobrania danych
    print("Podaj strone z tabelą \n")
    # url = 'https://vrsnet.pl/mapa_zasiegu.html'
    url = input()
    # Wysłanie żądania HTTP GET do strony
    response = requests.get(url)
    response.encoding = 'utf-8'  # Ustawienie odpowiedniego kodowania

    # Sprawdzenie, czy żądanie zakończyło się sukcesem
    if response.status_code == 200:
        # Parsowanie zawartości strony za pomocą BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Znalezienie wszystkich wierszy tabeli zawierających dane
        rows = soup.find_all('tr')

        # Iteracja przez wiersze i wyodrębnienie danych
        for row in rows:
            # Pominięcie wierszy zawierających colspan="8"
            if row.find('td', attrs={'colspan': '8'}):
                continue

            # Znalezienie wszystkich komórek w wierszu
            cells = row.find_all('td')
            if len(cells) > 0:
                # Wyodrębnienie danych z odpowiednich komórek
                miasto = cells[1].get_text(strip=True)
                wsp_xyz = cells[3].get_text(strip=True).replace('X:', '').strip().replace("Y:","    ").replace("Z:","    ").replace(": ","    ")

                # Wyświetlenie lub zapisanie danych
                print(f'{miasto}    {wsp_xyz}')
    else:
        print(f'Błąd podczas pobierania strony: {response.status_code}')

if __name__ == "__main__":
    main()