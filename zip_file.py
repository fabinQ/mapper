import os
import zipfile
from datetime import datetime

def create_zip_from_folder(folder_path, output_zip=None):
    """
    Create a ZIP file from a folder
    Args:
        folder_path (str): Path to the folder to be zipped
        output_zip (str): Optional name for output ZIP file
    """
    # If no output name specified, use folder name + timestamp
    folder_path = os.path.abspath(folder_path)
    if output_zip is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_zip = f"{os.path.basename(folder_path)}.zip"

    # Create zip file
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Walk through the folder
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                # Get full file path
                file_path = os.path.join(root, file)
                # Get relative path for zip structure
                rel_path = os.path.relpath(file_path, folder_path)
                # Add file to zip
                zipf.write(file_path, rel_path)

    return output_zip

if __name__ == "__main__":
    # Example usage
    folder_to_zip = ["C:\OneDrive - 3D GEOSYSTEMY MICHAŁ JAŚKIEWICZ\Projekty iCON Office\KB CONSTRUCTION\OSTRODA\Trimble\ostroda\Tor420dol20klinca202582B136-2592B431",
"C:\OneDrive - 3D GEOSYSTEMY MICHAŁ JAŚKIEWICZ\Projekty iCON Office\KB CONSTRUCTION\OSTRODA\Trimble\ostroda\Tor20820Dol20warstwy20ochronnej20korekta20na20palowanie2024.04.2025",
"C:\OneDrive - 3D GEOSYSTEMY MICHAŁ JAŚKIEWICZ\Projekty iCON Office\KB CONSTRUCTION\OSTRODA\Trimble\ostroda\Tor20220DC3B3C58220warstwy20ochronnej202572B859-2582B1802012.03.2025",
"C:\OneDrive - 3D GEOSYSTEMY MICHAŁ JAŚKIEWICZ\Projekty iCON Office\KB CONSTRUCTION\OSTRODA\Trimble\ostroda\Tor20220Dol20warstwy20ochronnej202572B859-2602B350",
"C:\OneDrive - 3D GEOSYSTEMY MICHAŁ JAŚKIEWICZ\Projekty iCON Office\KB CONSTRUCTION\OSTRODA\Trimble\ostroda\Tor20220GC3B3ra20warstwy20ochronnej202572B859-2582B1802012.03.2025",
"C:\OneDrive - 3D GEOSYSTEMY MICHAŁ JAŚKIEWICZ\Projekty iCON Office\KB CONSTRUCTION\OSTRODA\Trimble\ostroda\Tor20220Subwarstwa20-0.0820pod20podkladem202572B859-2582B180",
"C:\OneDrive - 3D GEOSYSTEMY MICHAŁ JAŚKIEWICZ\Projekty iCON Office\KB CONSTRUCTION\OSTRODA\Trimble\ostroda\Tor20420dol20klinca202582B136-2592B4312024.04.2025",
"C:\OneDrive - 3D GEOSYSTEMY MICHAŁ JAŚKIEWICZ\Projekty iCON Office\KB CONSTRUCTION\OSTRODA\Trimble\ostroda\Tor20620dol20warstwy20ochronnej20korekta20na20palowanie",
"C:\OneDrive - 3D GEOSYSTEMY MICHAŁ JAŚKIEWICZ\Projekty iCON Office\KB CONSTRUCTION\OSTRODA\Trimble\ostroda\Tor20620dol20warstwy20ochronnej20korekta20na20palowanie2024.04.2025",
"C:\OneDrive - 3D GEOSYSTEMY MICHAŁ JAŚKIEWICZ\Projekty iCON Office\KB CONSTRUCTION\OSTRODA\Trimble\ostroda\Tor20820Dol20warstwy20ochronnej20korekta20na20palowanie"]  # Replace with your folder path
    try:
        for folder in folder_to_zip:
            zip_file = create_zip_from_folder(folder)
            print(f"Successfully created ZIP file: {zip_file}")
    except Exception as e:
        print(f"Error creating ZIP file: {e}")