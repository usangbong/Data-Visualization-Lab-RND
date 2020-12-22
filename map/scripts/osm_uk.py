import csv
import json
from OSMPythonTools.nominatim import Nominatim

nominatim = Nominatim()
region_list = []
type_list = []
regions = {}
with open('./data/hidden/UK Coronavirus Cases 1112.csv') as csv_file:
  next(csv_file)
  reader = csv.reader(csv_file)
  for row in reader:
    region_name = row[0]
    region_postcode = row[1]
    region_type = row[2]

    if region_type not in type_list:
      type_list.append(region_type)
      regions[region_type] = []
    if region_name not in region_list:
      region_list.append(region_name)
      regions[region_type].append({
        'name': region_name,
        'type': region_type,
        'postcode': region_postcode
      })

for region_type in type_list:
  geodata = {
    'type': 'FeatureCollection',
    'features': []
  }
  for index, region in enumerate(regions[region_type]):
    osm = nominatim.query(f"{region['name']}, England")
    osm = osm.toJSON()[0]
    feature = {
      'type': 'Feature',
      'geometry': {
        'type': 'Point',
        'coordinates': [float(osm['lon']), float(osm['lat'])]
      },
      'properties': {
        'osmid': osm['osm_id'],
        'cell_id': index,
        'name': region['name'],
        'type': region['type'],
        'postcode': region['postcode']
      }
    }
    geodata['features'].append(feature)

  with open(f'./data/uk_{region_type}_osm.geojson', 'w', encoding='utf-8') as json_file:
    dump = json.dumps(geodata, ensure_ascii=False)
    json_file.write(dump)
    print(f'[osm-{region_type}] output:', len(geodata['features']))
