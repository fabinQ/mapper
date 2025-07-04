import os
import zipfile
from pathlib import Path

def compress_subfolders_to_zip(folder_path):
    """
    Kompresuje wszystkie podfoldery w podanej ścieżce do plików ZIP.
    Każdy podfolder zostanie skompresowany do pliku ZIP o tej samej nazwie.
    
    Args:
        folder_path (str): Ścieżka do folderu głównego
    """
    try:
        # Konwersja do obiektu Path dla łatwiejszej manipulacji
        main_folder = Path(folder_path)
        
        # Sprawdzenie czy podana ścieżka istnieje
        if not main_folder.exists():
            print(f"Błąd: Ścieżka '{folder_path}' nie istnieje!")
            return
        
        if not main_folder.is_dir():
            print(f"Błąd: '{folder_path}' nie jest folderem!")
            return
        
        # Znajdź wszystkie podfoldery
        subfolders = [item for item in main_folder.iterdir() 
                     if item.is_dir()]
        
        if not subfolders:
            print("Nie znaleziono żadnych podfolderów do kompresji.")
            return
        
        print(f"Znaleziono {len(subfolders)} podfolderów do kompresji...")
        
        # Kompresuj każdy podfolder
        for subfolder in subfolders:
            zip_filename = main_folder / f"{subfolder.name}.zip"
            
            print(f"Kompresowanie: {subfolder.name} -> {zip_filename.name}")
            
            try:
                with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    # Przejdź przez wszystkie pliki i podfoldery rekurencyjnie
                    for root, dirs, files in os.walk(subfolder):
                        for file in files:
                            file_path = Path(root) / file
                            # Oblicz względną ścieżkę względem kompresowanego folderu
                            arcname = file_path.relative_to(subfolder)
                            zipf.write(file_path, arcname)
                
                print(f"✓ Utworzono: {zip_filename.name}")
                
            except Exception as e:
                print(f"✗ Błąd podczas kompresji {subfolder.name}: {e}")
        
        print("\nKompresja zakończona!")
        
    except Exception as e:
        print(f"Błąd ogólny: {e}")

def main():
    """Główna funkcja programu"""
    print("=== KOMPRESJA PODFOLDERÓW DO ZIP ===\n")
    
    # Pobierz ścieżkę od użytkownika
    while True:
        folder_path = input("Podaj ścieżkę do folderu: ").strip()
        
        if folder_path:
            break
        else:
            print("Proszę podać prawidłową ścieżkę!")
    
    # Usuń cudzysłowy jeśli użytkownik je podał
    folder_path = folder_path.strip('"\'')
    
    # Wykonaj kompresję
    compress_subfolders_to_zip(folder_path)
    
    input("\nNaciśnij Enter aby zakończyć...")

if __name__ == "__main__":
    main()