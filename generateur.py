import json
import pandas as pd
import folium
from folium.plugins import MarkerCluster, LocateControl
from shapely import wkt
from shapely.geometry import shape, box
from folium import Popup
from bs4 import BeautifulSoup


def is_adjacent(geom):
    """
    Check if a geometry is adjacent to Oise using bounding box.
    """
    return box(*geom.bounds).intersects(oise_box_polygon)


def fish_icon():
    """
    Create a fish icon for markers.
    """
    return folium.DivIcon(
        html='<div style="font-size:24px;">🐟</div>',
        icon_size=(30, 30),
        icon_anchor=(20, 20)
    )


def generate_google_maps_link(lat, lon):
    """
    Create a Google Maps link using latitude and longitude.
    """
    return f"https://www.google.com/maps/@{lat},{lon},17z"


# Load data
with open('Lacs.json', encoding='utf-8') as f:
    lakes = json.load(f)
regions = pd.read_csv('Regions.csv', sep=';')

# https://geo.data.gouv.fr/fr/datasets/ee5c709c9b7ff928ab2529b79ce6e879c4de6950
with open('CoursEau_02_Rhin-Meuse.json', encoding='utf-8') as f:
    rivers = json.load(f)['features']

# Convert multipolygons WKT to Shapely format
regions['geometry'] = regions.iloc[:, 6].apply(wkt.loads)

# Find adjacent regions to Oise using bounding box
oise_polygon = regions[regions.iloc[:, 4] == "OISE"].iloc[0]['geometry']
oise_bbox = oise_polygon.bounds
oise_box_polygon = box(*oise_bbox)
adjacent_regions = regions[regions['geometry'].apply(is_adjacent)]

# Setup base map
oise_centroid = shape(oise_polygon).centroid.coords[0]
m = folium.Map(location=[oise_centroid[1], oise_centroid[0]], zoom_start=10, control_scale=False)
# titre de la page "La pêche réciprocitaire dans l'Oise"
m.get_root().html.add_child(folium.Element("<title>La pêche réciprocitaire dans l'Oise</title>"))
# Add Esri Satellite tile
folium.TileLayer(
    "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attr="Esri",
    name="Esri Satellite",
    overlay=False,
    control=True
).add_to(m)

# Add location control
LocateControl(flyTo=True, showPopup=True, locate_options={'enableHighAccuracy': True}).add_to(m)

# Add region outlines to the map (excluding Oise)
for _, region in regions.iterrows():
    if region.iloc[4] != 'OISE' and region.iloc[4] in adjacent_regions.iloc[:, 4].values:
        folium.GeoJson(
            region['geometry'],
            style_function=lambda x: {'color': 'lightgrey', 'fillOpacity': 0.2, 'weight': 1}
        ).add_to(m)

# Highlight Oise region
folium.GeoJson(
    oise_polygon,
    style_function=lambda x: {'color': 'white', 'fillOpacity': 0.05, 'weight': 1}
).add_to(m)

# Add river outlines to the map (linestrings)
for river in rivers:
    # on utilise shapely pour déterminer si le cours d'eau passe dans l'Oise
    if shape(river['geometry']).intersects(oise_polygon):
        # on pense à ajouter le nom NomEntiteH correspondant au cours d'eau quand on survole la ligne
        name = river['properties']['NomEntiteH']
        folium.GeoJson(
            river['geometry'],
            style_function=lambda x: {'color': 'darkblue', 'fillOpacity': 1, 'weight': 4},
            tooltip=name
        ).add_to(m)


# Marker cluster configurations
icon_create_function = """
function(cluster) {
    return L.divIcon({
        html: `
            <div style="position: relative; width: 70px; height: 60px;">
                <div style="position: absolute; top: 0; left: 50%; transform: translateX(-50%); font-size: 30px;">🐟</div>
                <div style="position: absolute; bottom: 0; left: 0; font-size: 30px;">🐟</div>
                <div style="position: absolute; bottom: 0; right: 0; font-size: 30px;">🐟</div>
            </div>
            ` + cluster.getChildCount(),
        className: 'marker-cluster',
        iconSize: new L.Point(60, 60),
        iconAnchor: new L.Point(70, 70)
    });
}
"""
marker_cluster = MarkerCluster(icon_create_function=icon_create_function, options={'maxClusterRadius': 30}).add_to(m)

# Add lake markers and polygons
for lake in lakes:
    coords = shape(lake['geometry']).centroid.coords[0]
    name = lake['properties']['nom']
    link = lake['properties']['lien']

    # Adjust name for display
    if len(name) > 20:
        space_index = name[25:].find(' ')
        if space_index != -1:
            name = name[:25 + space_index] + '<br>' + name[25 + space_index:]

    google_maps_link = generate_google_maps_link(coords[1], coords[0])
    custom_popup = Popup(
        f"Nom: {name}<br>Règlement: <a href='{link}'>Lien</a><br>Catégorie: 2<br>Carte: <a href='{google_maps_link}' target='_blank'>Voir sur Maps</a>",
        max_width=400
    )

    folium.Marker([coords[1], coords[0]], icon=fish_icon(), popup=custom_popup).add_to(marker_cluster)
    folium.GeoJson(lake, style_function=lambda x: {'color': 'lightblue', 'fillOpacity': 0.5}).add_to(m)

m.save('map.html')


# Ouvrir le fichier map.html
with open('map.html', 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')

# Ajouter une barre en haut pour la publicité
header_html = """
<style>
    @media (max-width: 600px) {
        .header-bar span, .header-bar a, .header-bar button, .info-tooltip {
            font-size: 12px;
            padding: 2px 6px;
        }
        .header-bar, .ad-bar {
            padding: 5px 0px;
            flex-direction: column;
            align-items: center;
        }
        .header-bar .link-group {
            display: flex;
            justify-content: center;
            gap: 5px;
            margin-top: 5px;
        }
    }
    .info-tooltip {
        position: relative;
        margin-left: 5px; /* Ajout d'une marge à gauche pour éloigner l'icône du texte */
    }
    .info-tooltip-content {
        display: none;
        position: absolute;
        left: 100%;
        top: 0;
        width: 250px;
        background-color: #fff;
        border: 1px solid #ccc;
        padding: 8px;
        font-size: 14px;
        z-index: 9999;
        border-radius: 5px;
    }
    .info-tooltip:hover .info-tooltip-content {
        display: block;
    }
</style>

<div class="header-bar" style="background-color: #f5f5f5; padding: 8px 0px; border-bottom: 1px solid #e0e0e0; font-family: Arial; text-align: center; display: flex; justify-content: center; align-items: center;">
    <span style="flex: 1; text-align: left; margin-left: 10px;">
        Vous souhaitez réaliser une carte dans ce style ou contribuer?
        <span class="info-tooltip">
            ℹ️ 
            <div class="info-tooltip-content">
                Cette carte présente les lieux de pêche réciprocitaires.<br>
                Elle est en cours de construction.<br>
            </div>
        </span>
    </span>
    
    <div class="link-group">
        <span style="margin-right: 5px;">
            🌐 <a href="https://webanimus.com" style="color: #0077b5; text-decoration: none; padding: 4px 8px; border: 1px solid #0077b5; border-radius: 5px;">Webanimus</a> 
        </span>
        
        <span style="margin-right: 5px;">
            📧 <a href="mailto:clement.girard@webanimus.com" style="color: #0077b5; text-decoration: none; padding: 4px 8px; border: 1px solid #0077b5; border-radius: 5px;">E-mail</a>
        </span>
        
        <span style="margin-right: 15px;">
            ☕ <a href="https://paypal.me/webanimus" target="_blank" style="color: #0070ba; text-decoration: none; padding: 4px 8px; border: 1px solid #0070ba; border-radius: 5px;">Café</a>
        </span>
    </div>
</div>

"""

# Insérer le bandeau en haut de la carte
soup.body.insert(0, BeautifulSoup(header_html, 'html.parser'))

# Ajouter le style pour désactiver le défilement
style_tag = soup.new_tag('style')
style_content = """
body {
    overflow: hidden;  /* Empêche le défilement */
}
"""
style_tag.string = style_content
soup.head.append(style_tag)

# Styliser la carte pour qu'elle soit juste en dessous du bandeau
map_div = soup.find("div", {"style": "position:relative;width:100%;height:0;padding-bottom:60%;"})
if map_div:
    map_div["style"] = "position:relative;width:100%;height:calc(100vh - 50px);"

# Sauvegarder les modifications
with open('map.html', 'w', encoding='utf-8') as file:
    file.write(str(soup))

