import folium
import pandas as pd
from geopy.geocoders import ArcGIS
import random
import os
from folium.plugins.mat_icon import MatIcon

geo_locator = ArcGIS(timeout=10)
save_file_check = '\\', '/', '>', '<', '*', '?', '|', '"', '*', '\n'
column_check = 'address', 'city', 'state', 'longitude', 'latitude'
default_icons = ('search-plus', 'share', 'shopping-basket', 'star', 'suitcase', 'thumb-tack',
                 'tags', 'pencil', 'location-arrow', 'map-pin', 'map')
available_colors = ('\npurple', 'white', 'darkgreen', 'lightgray', 'beige',
                    '\nlightblue', 'red', 'darkpurple', 'gray', 'orange', 'blue',
                    '\ngreen', 'cadetblue', 'darkred', 'lightgreen', 'lightred',
                    '\npink', 'black', 'darkblue\n')
map_layers = []
lat_list = []
lon_list = []


class MapLayer:

    def __init__(self, layer='', data_frame='', lat_lon_available='',
                 label='', icon_color='', icon='', marker_color='',
                 marker_outline_color='', marker_outline_width=''):

        self.layer = layer
        self.data_frame = data_frame
        self.lat_lon_available = lat_lon_available
        self.label = label
        self.icon_color = icon_color
        self.icon = icon
        self.marker_color = marker_color
        self.marker_outline_color = marker_outline_color
        self.marker_outline_width = marker_outline_width

    def layer_attributes(self):
        layer_name = ''
        while len(layer_name) == 0:
            layer_name = input('Enter a name for the map layer of this data set:\n')

        label = input('Enter the name of the column that contains the information\n'
                      'to be shown in each marker label.\n'
                      'Or press enter to use the location as the label:\n').lower()

        while label not in self.data_frame.columns:
            if len(label) == 0:
                break
            label = input('That label was not found in your file.\nEnter the correct'
                          ' column name or press Enter to use the location as label:\n').lower()

        defaults = ''
        while defaults != 'yes' and defaults != 'no':
            defaults = input('Do you want the marker icons and colors to be set to default? yes or no: \n')

        self.layer = folium.FeatureGroup(name=layer_name)
        self.label = label
        self.create_icons(defaults)

    def add_markers(self):
        if self.lat_lon_available == 'False':
            for row in range(self.data_frame.shape[0]):
                self.layer.add_child(folium.Marker(
                    location=self.get_lat_lon(row),
                    popup=(self.add_label(row)),
                    icon=MatIcon(marker_color=self.marker_color,
                                 marker_outline_color=self.marker_outline_color,
                                 marker_outline_width=self.marker_outline_width,
                                 icon_color=self.icon_color,
                                 icon=self.icon)
                ))
        else:
            for row in range(self.data_frame.shape[0]):
                lat_list.append(self.data_frame['latitude'][row])
                lon_list.append(self.data_frame['longitude'][row])
                self.layer.add_child(folium.Marker(
                    location=[self.data_frame['latitude'][row], self.data_frame['longitude'][row]],
                    popup=(self.add_label(row)),
                    icon=MatIcon(marker_color=self.marker_color,
                                 marker_outline_color=self.marker_outline_color,
                                 marker_outline_width=self.marker_outline_width,
                                 icon_color=self.icon_color,
                                 icon=self.icon)
                ))

    def get_lat_lon(self, row):
        geo_location = geo_locator.geocode('{},{},{}'.format(
            self.data_frame['address'][row],
            self.data_frame['city'][row],
            self.data_frame['state'][row], ))
        lat_lon = [geo_location.latitude, geo_location.longitude]
        lat_list.append(lat_lon[0])
        lon_list.append(lat_lon[1])
        return lat_lon

    def add_label(self, row):
        if len(self.label) > 0:
            return str(self.data_frame[self.label][row])

        elif 'latitude' in self.data_frame.columns:
            return "{},\n{},".format(
                self.data_frame['latitude'][row],
                self.data_frame['longitude'][row], )

        else:
            return "{},\n{},\n{},".format(
                self.data_frame['address'][row],
                self.data_frame['city'][row],
                self.data_frame['state'][row])

    def create_icons(self, defaults):
        if defaults == 'no':
            self.icon = input('You can choose an icon you like from '
                              'https://fontawesome.com/v4.7.0/icons/\n'
                              'Just enter the name of the icon here:\n').lower()
            print('\nPlease select one of the following colors:\n'
                  '{}'.format(", ".join(available_colors).title()))
            self.marker_color = input('Enter a color for the Marker: ').lower()
            self.icon_color = input('Enter a color for the Icon: ').lower()
            self.marker_outline_width = input('Enter a width for the marker outline: ').lower()
            self.marker_outline_color = input('Enter a color for the marker outline: ').lower()
            return

        self.marker_color = random.choice(available_colors)
        self.icon = random.choice(default_icons)
        self.icon_color = 'white'


def data_input():
    print('\nWelcome to Python Map Maker.\n'
          '\nThis program can process your data sets and plot them in\n'
          'a map using markers and labels with information.\n'
          'This program accepts multiple csv data sets, and it will create a layer on\n'
          'the map for each data set. You can also toggle the layers on and off\n\n'
          'The csv data set will need the following columns:\n'
          'Address, City, State, or Latitude and Longitude. The column for\n'
          'the label information is optional. You will enter\n'
          'the name for this column when the layer is created.\n'
          )

    while True:

        file_check()
        map_layers[-1].layer_attributes()
        add_another_file = input('Do you wish to add another file? yes or no: \n')

        while add_another_file != 'yes' and add_another_file != 'no':
            add_another_file = input('\nDo you wish to add another file? yes or no: \n')

        if add_another_file == 'no':
            break
    print('Please wait while your map is being generated\n')
    create_map()


def file_check():
    file_name = ''
    while len(file_name) == 0:
        file_name = input('Please enter the csv file containing your data:\n')
    if len(file_name) > 0:
        try:
            map_layers.append(MapLayer(data_frame=pd.read_csv(file_name)))
        except:
            print('The file does not exists in the current directory')
            file_check()
    map_layers[-1].data_frame.columns = map(str.lower, map_layers[-1].data_frame.columns)
    for lat_lon_column in column_check[-2:]:

        if lat_lon_column not in map_layers[-1].data_frame.columns:
            for add_city_st_column in column_check[:2]:

                if add_city_st_column not in map_layers[-1].data_frame.columns:
                    print('This Data Set does not contain a {} column\n'
                          .format(add_city_st_column.capitalize()),
                          'Address, City, State, or Longitude and '
                          'Latitude columns are required.\n')
                    map_layers.remove(map_layers[-1])
                    file_check()
            map_layers[-1].lat_lon_available = 'False'
            return
    map_layers[-1].lat_lon_available = 'True'
    return


def create_map():
    for map_layer in map_layers:
        map_layer.add_markers()
    map_base = folium.Map(location=map_location(), zoom_start=zoom_start(),
                          tiles='CartoDB positron')
    for map_layer in map_layers:
        map_base.add_child(map_layer.layer)
    map_base.add_child(folium.LayerControl())
    map_name = save_file_name_check()
    map_base.save('{}.html'.format(map_name))
    os.startfile('{}.html'.format(map_name))


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
        zoom = 5
    return zoom


def save_file_name_check():
    map_name = input('Please enter your map name to be saved.\n'
                     'Do not use characters \\ / > < * ? | " :')
    for character in save_file_check:
        if character in map_name:
            save_file_name_check()
    if len(map_name) == 0:
        save_file_name_check()
    return map_name


if __name__ == '__main__':
    data_input()
