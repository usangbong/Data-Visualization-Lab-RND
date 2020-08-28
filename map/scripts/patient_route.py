import pandas as pd
import geopandas as gpd
import numpy as np
import pyproj
from fiona.crs import from_epsg

voronoi = gpd.read_file('data/kr_village_voronoi.json')

route_original = gpd.read_file('data/hidden/patient_route_0818.csv')
route = route_original
route = route.replace('', np.nan)[['Latitude', 'Longitude']].dropna()
route_geom = gpd.points_from_xy(route.Longitude, route.Latitude)
route_frame = gpd.GeoDataFrame(route, geometry=route_geom, crs=from_epsg(4326))

emdllist = {}
for index, row in route_frame.iterrows():
    emdllist[index] = list(voronoi[voronoi.contains(row.geometry)]['emdlid'])[0]
series = pd.Series(list(emdllist.values()), index=list(emdllist.keys()), dtype=np.dtype("int32"))
route_frame.assign(emdlid=series)
print(route_frame)
