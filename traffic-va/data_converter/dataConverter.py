import json

with open('route_data_original.json', encoding='utf-8') as route_file:
    route_data = json.load(route_file)

convertedData = {}
for data in route_data:
    new_data = {}
    new_data_name = ''
    new_data_coord = []
    if data['roundtrip'] == 1:
        place_split = data['name'].split('-')
        new_data_reverse = {}
        new_data_name = place_split[1] + '-' + place_split[0]
        new_data_coord = []
        for coordinate in data['coordinates']:
            new_data_coord.insert(0, coordinate)

        new_data_reverse['coordinates'] = []
        for coord in new_data_coord:
            new_data_reverse['coordinates'].append([coord[1], coord[0]])

        convertedData[new_data_name] = new_data_reverse

    new_data_name = data['name']
    new_data_coord = data['coordinates']
    
    new_data['coordinates'] = []
    for coord in new_data_coord:
        new_data['coordinates'].append([coord[1], coord[0]])

    convertedData[new_data_name] = new_data

with open('./route_data.json', 'w', encoding='utf-8') as make_file:
    json.dump(convertedData, make_file, indent='  ', ensure_ascii=False)