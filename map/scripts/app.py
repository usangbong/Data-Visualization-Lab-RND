import json

with open('data/EMD.json', encoding="utf-8") as json_file:
  data = json.load(json_file)
  for feature in data.features:
    properties = feature.properties
    geometry = feature.geometry
    for 