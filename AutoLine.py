import json
import numpy as np
from shapely.geometry import LineString, mapping
from lxml import etree

# Import funkcji
def calculate_azimuth(point1, point2):
    delta_x = point2[0] - point1[0]
    delta_y = point2[1] - point1[1]
    angle = np.arctan2(delta_y, delta_x) * 180 / np.pi
    return angle % 360

def extract_lines(geometry):
    if geometry.geom_type == 'MultiLineString':
        return list(geometry)
    elif geometry.geom_type == 'LineString':
        return [geometry]
    else:
        return []

def merge_lines(lines):
    merged_line = LineString()
    for line in lines:
        if merged_line.is_empty:
            merged_line = line
        else:
            merged_line = merged_line.union(line)
    return merged_line


def export_to_geojson(geometry, filename="output.geojson"):
    """
    Eksportuje geometrię do formatu GeoJSON.
    """
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    # Obsługa różnych typów geometrii
    if geometry.geom_type == 'MultiLineString':
        for line in geometry.geoms:  # Poprawka: użycie geometry.geoms
            geojson["features"].append({
                "type": "Feature",
                "geometry": mapping(line),
                "properties": {}
            })
    elif geometry.geom_type == 'LineString':
        geojson["features"].append({
            "type": "Feature",
            "geometry": mapping(geometry),
            "properties": {}
        })
    else:
        raise TypeError(f"Nieobsługiwany typ geometrii: {geometry.geom_type}")

    # Zapis GeoJSON do pliku
    file_path = filename
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(geojson, f, indent=2)
    return file_path


def export_to_geojson_swap_coords(geometry, filename="swapped_output.geojson"):
    """
    Eksportuje geometrię do formatu GeoJSON z zamianą współrzędnych X i Y.
    """
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    # Obsługa różnych typów geometrii
    if geometry.geom_type == 'MultiLineString':
        for line in geometry.geoms:  # Poprawka: użycie geometry.geoms
            swapped_coords = [(y, x) for x, y in line.coords]
            geojson["features"].append({
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": swapped_coords
                },
                "properties": {}
            })
    elif geometry.geom_type == 'LineString':
        swapped_coords = [(y, x) for x, y in geometry.coords]
        geojson["features"].append({
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": swapped_coords
            },
            "properties": {}
        })
    else:
        raise TypeError(f"Nieobsługiwany typ geometrii: {geometry.geom_type}")

    # Zapis GeoJSON do pliku
    file_path = filename
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(geojson, f, indent=2)
    return file_path


def create_landxml(merged_line, filename="output.xml"):
    """
    Tworzy plik LandXML zawierający połączoną linię równoległą.
    Obsługuje zarówno LineString, jak i MultiLineString.
    """
    root = etree.Element("LandXML", xmlns="http://www.landxml.org/schema/LandXML-1.2", version="1.2")
    doc = etree.SubElement(root, "Document")
    doc.text = "Eksport z analizy linii równoległych"

    alignments = etree.SubElement(root, "Alignments")
    alignment = etree.SubElement(alignments, "Alignment", name="MergedParallelLine")
    coordGeom = etree.SubElement(alignment, "CoordGeom")

    # Obsługa MultiLineString
    if merged_line.geom_type == 'MultiLineString':
        for sub_line in merged_line.geoms:
            line_element = etree.SubElement(coordGeom, "Line")
            coords = list(sub_line.coords)
            for i, coord in enumerate(coords[:-1]):  # Wszystkie punkty oprócz ostatniego
                etree.SubElement(line_element, "Start", x=str(coord[0]), y=str(coord[1]))
            # Dodanie końca ostatniego segmentu
            etree.SubElement(line_element, "End", x=str(coords[-1][0]), y=str(coords[-1][1]))

    # Obsługa LineString
    elif merged_line.geom_type == 'LineString':
        line_element = etree.SubElement(coordGeom, "Line")
        coords = list(merged_line.coords)
        for i, coord in enumerate(coords[:-1]):  # Wszystkie punkty oprócz ostatniego
            etree.SubElement(line_element, "Start", x=str(coord[0]), y=str(coord[1]))
        # Dodanie końca ostatniego segmentu
        etree.SubElement(line_element, "End", x=str(coords[-1][0]), y=str(coords[-1][1]))

    else:
        raise TypeError(f"Nieobsługiwany typ geometrii: {merged_line.geom_type}")

    # Zapis pliku
    file_path = filename
    tree = etree.ElementTree(root)
    tree.write(file_path, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    return file_path


# Kod główny
def main(file_path, output_dir):
    # Wczytanie pliku
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.readlines()

    # Wyszukiwanie sekcji LineList
    start_line_list = file_content.index('LineList \n') + 2
    end_line_list = file_content.index('end\n', start_line_list)
    line_list_section = file_content[start_line_list:end_line_list]

    # Parsowanie linii
    lines_data = []
    current_line = None
    current_points = []
    for line in line_list_section:
        if line.startswith('\tLine'):
            if current_line is not None:
                lines_data.append({"line": current_line, "points": current_points})
            current_line = line.strip()
            current_points = []
        elif line.startswith('\t\t\tPoint'):
            parts = line.split(',')
            try:
                x = float(parts[1])
                y = float(parts[2])
                current_points.append((x, y))
            except (IndexError, ValueError):
                continue
    if current_line is not None:
        lines_data.append({"line": current_line, "points": current_points})

    # Analiza linii bazowej
    base_line_points = [(6021536.17668504, 6521431.07019169), (6021519.92792903, 6521421.8076452)]
    base_azimuths = [calculate_azimuth(base_line_points[i], base_line_points[i + 1]) for i in range(len(base_line_points) - 1)]
    average_base_azimuth = np.mean(base_azimuths)

    # Filtracja linii równoległych
    tolerance = 25
    parallel_lines = []
    for line in lines_data:
        points = line["points"]
        if len(points) > 1:
            azimuths = [calculate_azimuth(points[i], points[i + 1]) for i in range(len(points) - 1)]
            average_azimuth = np.mean(azimuths)
            if abs(average_azimuth - average_base_azimuth) <= tolerance:
                parallel_lines.append(LineString(points))

    # Łączenie linii
    merged_lines = merge_lines(parallel_lines)

    # Eksport do GeoJSON
    geojson_path = export_to_geojson(merged_lines, filename=f"{output_dir}/MergedParallelLines.geojson")

    # Eksport do GeoJSON z zamianą współrzędnych
    swapped_geojson_path = export_to_geojson_swap_coords(merged_lines, filename=f"{output_dir}/SwappedMergedParallelLines.geojson")

    # Eksport do LandXML
    landxml_path = create_landxml(merged_lines, filename=f"{output_dir}/MergedParallelLines.xml")

    print("Eksport zakończony:")
    print(f"GeoJSON: {geojson_path}")
    print(f"Swapped GeoJSON: {swapped_geojson_path}")
    print(f"LandXML: {landxml_path}")

# Uruchomienie programu
main("geo_files/Sytuacja 2D Glincza rozjazd południowy.geo", "geo_files")
