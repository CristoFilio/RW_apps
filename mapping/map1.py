import folium
import pandas as pd
from geopy.geocoders import ArcGIS

finder = ArcGIS(timeout=10)
df1 = pd.read_csv('../pandas/hospitals.csv')
markers = folium.FeatureGroup(name=input('Enter the marker layer name:'))

lat_list = []
lon_list = []


def get_lat_lon(num):
    geo_loc = finder.geocode('{},{},{}'.format(
        df1['Address'][num],
        df1['City'][num],
        df1['State'][num], ))
    lat_lon = [geo_loc.latitude, geo_loc.longitude]
    lat_list.append(lat_lon[0])
    lon_list.append(lat_lon[1])
    return lat_lon


def labels(num):
    label = ''
    for column in df1.columns:
        if column.lower() == 'label':
            label = column
            break
    if len(label) > 0:
        return str(df1[label][num])
    else:
        return "{},\n{},\n{},".format(
                df1['Address'][num],
                df1['City'][num],
                df1['State'][num])


def add_markers():
    for num in range(df1.shape[0]):
        markers.add_child(folium.Marker(location=get_lat_lon(num),
                                        popup=(labels(num))
                                        ))


def map_location():
    lat = sum(lat_list) / len(lat_list)
    lon = sum(lon_list) / len(lon_list)
    return [lat, lon]


def zoom_start():
    distance = max(lon_list) - min(lon_list)
    if distance < 0.05:
        zoom = 20
    if 0.05 < distance < 0.10:
        zoom = 16
    if 0.10 < distance < 0.20:
        zoom = 15
    if distance > 1:
        zoom = 4
    return zoom


def create_map():
    add_markers()
    map_one = folium.Map(location=map_location(), zoom_start=zoom_start(),
                         tiles='OpenStreetMap')
    map_one.add_child(markers)
    map_one.save('Map1.html')


create_map()
