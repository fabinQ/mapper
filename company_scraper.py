import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urljoin
import json # Potrzebne do przetwarzania danych JSON
import re   # Potrzebne do wyciągnięcia danych ze skryptu

# --- Konfiguracja (bez zmian) ---
PLIK_Z_URLAMI = 'firmy.txt'
PLIK_WYNIKOWY_CSV = 'firmy_geodezyjne_szczegolowe.csv'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def pobierz_urls_z_pliku(nazwa_pliku):
    """Wczytuje listę adresów URL z pliku tekstowego."""
    try:
        with open(nazwa_pliku, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
        return urls
    except FileNotFoundError:
        print(f"Błąd: Nie znaleziono pliku '{nazwa_pliku}'!")
        return []

def zbierz_linki_do_profili(lista_url):
    """
    Etap 1: Odwiedza strony z listami firm i zbiera linki do ich indywidualnych profili.
    """
    linki_profili = set()
    print("--- ETAP 1: Zbieranie linków do profili firm ---")
    for url in lista_url:
        print(f"Przetwarzam listę: {url}")
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            linki_na_stronie = soup.select('a.company-name')
            for link in linki_na_stronie:
                if link.has_attr('href'):
                    pelny_link = urljoin(url, link['href'])
                    linki_profili.add(pelny_link)
            print(f"  Znaleziono {len(linki_na_stronie)} linków na tej stronie.")
            time.sleep(1)
        except requests.RequestException as e:
            print(f"  Nie udało się pobrać strony {url}. Błąd: {e}")
            
    print(f"\nZebrano łącznie {len(linki_profili)} unikalnych linków do profili.\n")
    return list(linki_profili)


def scrapuj_profil_firmy(url_profilu):
    """
    Etap 2: Pobiera szczegółowe dane z indywidualnej strony profilowej firmy,
    wyciągając dane JSON ze skryptu.
    """
    try:
        response = requests.get(url_profilu, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Znajdź wszystkie tagi <script>
        scripts = soup.find_all('script', type='text/javascript')
        
        company_data = None
        for script in scripts:
            # Sprawdzamy, czy w skrypcie znajduje się poszukiwana zmienna
            if script.string and 'var company = {' in script.string:
                # Używamy wyrażenia regularnego, aby wyciągnąć obiekt JSON
                match = re.search(r'var company = ({.*?});', script.string, re.DOTALL)
                if match:
                    json_str = match.group(1)
                    # Konwertujemy tekst (string) na obiekt Pythona (słownik)
                    company_data = json.loads(json_str)
                    break # Znaleźliśmy dane, więc przerywamy pętlę
        
        if company_data:
            # Wyciągamy dane ze słownika, każdy element w osobnym try-except
            try:
                nazwa = company_data.get('name', 'Brak nazwy')
            except Exception:
                nazwa = 'Brak nazwy'
            try:
                nip = company_data.get('nip', 'Brak NIP')
            except Exception:
                nip = 'Brak NIP'
            try:
                contact = company_data.get('contact', {})
            except Exception:
                contact = {}
            try:
                strona_www = contact.get('www', 'Brak strony WWW')
            except Exception:
                strona_www = 'Brak strony WWW'
            try:
                email = contact.get('email', 'Brak e-maila')
            except Exception:
                email = 'Brak e-maila'
            try:
                phone_info = contact.get('phone', {})
                telefon = phone_info.get('number', 'Brak telefonu')
            except Exception:
                telefon = 'Brak telefonu'
            try:
                social_links = company_data.get('socialLinks', {})
                facebook = social_links.get('facebook', [None])[0] or 'Brak Facebooka'
            except Exception:
                facebook = 'Brak Facebooka'

            return [nazwa, nip, telefon, strona_www, email, facebook, url_profilu]
        else:
            print(f"  Nie znaleziono danych JSON na stronie: {url_profilu}")
            return None

    except requests.RequestException as e:
        print(f"  Nie udało się pobrać profilu {url_profilu}. Błąd: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"  Błąd przetwarzania danych JSON na stronie: {url_profilu}. Błąd: {e}")
        return None

# --- Główna część skryptu (bez zmian) ---
def main():
    strony_z_listami = pobierz_urls_z_pliku(PLIK_Z_URLAMI)
    
    if strony_z_listami:
        # ETAP 1
        linki_do_profili_firm = zbierz_linki_do_profili(strony_z_listami)
        
        if not linki_do_profili_firm:
            print("Nie znaleziono żadnych linków do profili. Kończę pracę.")
        else:
            # ETAP 2
            print("--- ETAP 2: Pobieranie szczegółowych danych z profili ---")
            wszystkie_firmy = []
            licznik = 1
            for link in linki_do_profili_firm:
                print(f"Pobieram dane ({licznik}/{len(linki_do_profili_firm)}): {link}")
                dane = scrapuj_profil_firmy(link)
                if dane:
                    wszystkie_firmy.append(dane)
                # time.sleep(1) # Przerwa
                licznik += 1

            # Zapis do pliku CSV
            try:
                with open(PLIK_WYNIKOWY_CSV, 'w', newline='', encoding='utf-8-sig') as plik_csv:
                    writer = csv.writer(plik_csv)
                    writer.writerow(['Nazwa Firmy', 'NIP', 'Telefon', 'Strona WWW', 'Email', 'Facebook', 'Link do profilu PF'])
                    writer.writerows(wszystkie_firmy)
                print(f"\nUkończono! Zapisano dane {len(wszystkie_firmy)} firm do pliku '{PLIK_WYNIKOWY_CSV}'.")
            except IOError as e:
                print(f"Błąd zapisu do pliku CSV: {e}")
if __name__ == "__main__":
    main()