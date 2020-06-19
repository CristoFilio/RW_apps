import folium
import pandas as pd
from geopy.geocoders import ArcGIS
import random

finder = ArcGIS(timeout=10)
string_check = '\\', '/', '>', '<', '*', '?', '|', '"', '*', '\n'
column_check = 'address', 'city', 'state', 'longitude', 'latitude'
icon_options = ('search-plus', 'share', 'shopping-basket', 'star', 'suitcase', 'thumb-tack',
                'tags', 'pencil', 'location-arrow', 'map-pin', 'map')
marker_colors = 'purple', 'white', 'darkgreen', 'lightgray', 'beige', \
                'lightblue', 'red', 'darkpurple', 'gray', 'orange', 'blue', \
                'green', 'cadetblue', 'darkred', 'lightgreen', 'lightred', \
                'pink', 'black', 'darkblue'
data_frames = []
layers = []
lat_list = []
lon_list = []
lat_lon_available = []


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


def get_lat_lon(num, data_frame):
    geo_loc = finder.geocode('{},{},{}'.format(
        data_frame['address'][num],
        data_frame['city'][num],
        data_frame['state'][num], ))
    lat_lon = [geo_loc.latitude, geo_loc.longitude]
    lat_list.append(lat_lon[0])
    lon_list.append(lat_lon[1])
    return lat_lon


def create_icon(defaults):
    if defaults == 'no':
        icon = input('You can choose an icon you like from '
                     'https://fontawesome.com/v4.7.0/icons/\n'
                     'Just enter the name of the icon here: ')
        print('\nPlease select one of the following colors:\n'
              '{}'.format(marker_colors))
        color = input('Enter a color for the Marker: ')
        icon_color = input('Enter a color for the Icon: ')
        return color, icon_color, icon
    color = random.choice(marker_colors)
    icon = random.choice(icon_options)
    icon_color = 'white'
    return color, icon_color, icon


def labels(num, data_frame, current_layer):
    if len(layers[current_layer][1]) > 0:
        label = layers[current_layer][1]
        return str(data_frame[label][num])
    elif 'latitude' in data_frame.columns:
        return "{},\n{},".format(
            data_frame['latitude'][num],
            data_frame['longitude'][num], )

    else:
        return "{},\n{},\n{},".format(
            data_frame['address'][num],
            data_frame['city'][num],
            data_frame['state'][num])


def add_markers():
    current_layer = 0
    for data_frame in data_frames:

        if lat_lon_available[current_layer] == 'False':

            for num in range(data_frame.shape[0]):
                layers[current_layer][0].add_child(folium.Marker(
                    location=get_lat_lon(num, data_frame),
                    popup=(labels(num, data_frame, current_layer)),
                    icon=folium.Icon(color=layers[current_layer][2][0],
                                     icon_color=layers[current_layer][2][1],
                                     icon=layers[current_layer][2][2],
                                     prefix='fa')
                ))
            current_layer += 1
        else:
            for num in range(data_frame.shape[0]):
                lat_list.append(data_frame['latitude'][num])
                lon_list.append(data_frame['longitude'][num])

                layers[current_layer][0].add_child(folium.Marker(
                    location=[data_frame['latitude'][num], data_frame['longitude'][num]],
                    popup=(labels(num, data_frame, current_layer)),
                    icon=folium.Icon(color=layers[current_layer][2][0],
                                     icon_color=layers[current_layer][2][1],
                                     icon=layers[current_layer][2][2],
                                     prefix='fa')
                ))
            current_layer += 1


def file_name_check():
    map_name = input('Please enter your map name to be saved.\n'
                     'Do not use characters \\ / > < * ? | " :')
    for character in string_check:
        if character in map_name:
            file_name_check()
    if len(map_name) == 0:
        file_name_check()
    return map_name


def create_map():
    add_markers()
    map_one = folium.Map(location=map_location(), zoom_start=zoom_start(),
                         tiles='CartoDB positron')
    for marker in layers:
        map_one.add_child(marker[0])
    map_one.add_child(folium.LayerControl())
    map_name = file_name_check()
    map_one.save('{}.html'.format(map_name))


def create_layer():
    layer_name = ''
    while len(layer_name) == 0:
        layer_name = input('Enter a name for the map layer of this data set:\n')

    label = input('\nEnter the name of the column that contains the information\n'
                  'to be shown in each marker label.\n'
                  'Or press enter to use the location as the label:\n').lower()

    while label not in data_frames[-1].columns:
        if len(label) == 0:
            break
        label = input('That label was not found in your file.\nEnter the correct'
                      ' column name or press Enter to use the location as label:\n').lower()

    defaults = ''
    while defaults != 'yes' and defaults != 'no':
        defaults = input('Do you want the marker icons and colors to be set to default? yes or no: \n')

    icon_choice = create_icon(defaults)
    layers.append((folium.FeatureGroup(name=layer_name), label, icon_choice))


def file_check():
    file_name = ''
    while len(file_name) == 0:
        file_name = input('\nPlease enter the file containing your data:\n')
    if len(file_name) > 0:
        try:
            data_frames.append(pd.read_csv(file_name))
        except:
            print('The file does not exists in the current directory')
            file_check()
    data_frames[-1].columns = map(str.lower, data_frames[-1].columns)
    for lat_lon_check in column_check[-2:]:

        if lat_lon_check not in data_frames[-1].columns:
            for acs_check in column_check[:2]:

                if acs_check not in data_frames[-1]:
                    print('This Data Set does not contain a {} column\n'
                          .format(acs_check.capitalize()),
                          'Address, City, State, or Longitude and '
                          'Latitude columns are required.\n')
                    data_frames.remove(data_frames[-1])
                    file_check()

            lat_lon_available.append('False')
            return
    lat_lon_available.append('True')
    return


def data_input():
    print('Welcome to Python Map Maker.\n'
          'This program can process your data sets and plot them in\n'
          'a map using markers and labels with information.\n'
          'This program accepts multiple data sets, and it will create a layer on\n'
          'the map for each data set. You can also toggle the layers on and off\n\n'
          'The data set will need the following columns:\n'
          'Address, City, State, or Latitude and Longitude. The column for\n'
          'the label information is optional. You will enter\n'
          'the name for this column when the layer is created.'
          )

    while True:

        file_check()
        create_layer()
        add_another_file = input('Do you wish to add another file? yes or no: \n')

        while add_another_file != 'yes' and add_another_file != 'no':
            add_another_file = input('Do you wish to add another file? yes or no: \n')

        if add_another_file == 'no':
            break
    print('Please wait while your map is being generated\n')
    create_map()


if __name__ == '__main__':
    data_input()
