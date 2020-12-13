import json
import geopandas as gpd
import random
import string
import numpy as np
from shapely.geometry import box
import itertools
import pandas as pd

EPSG_WGS84 = 'EPSG:4326'
EPSG_UTM32V = 'EPSG:32632'

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def clean_response(json_response):
    if('bbox' in json_response): del json_response['bbox']
    if('bbox' in json_response['features'][0]): 
        for i in range(0, len(json_response['features'])):
            del json_response['features'][i]['bbox'] # assumes only one feature in the collection
    return json_response


def buffer(geoframe, value):
    # convert to UTM32 for reference system in meters
    data_utm32V = convert_to_UTM_32V(geoframe)

    # apply buffer
    data_utm32V_buffer = data_utm32V.buffer(value)

    # convert back to WGS84
    data_wgs84_buffer = convert_to_WGS84(data_utm32V_buffer)

    data_wgs84_buffer_json = json.loads(data_wgs84_buffer.to_json())

    return clean_response(data_wgs84_buffer_json)

def union(geoframe):
    print(geoframe)
    union = geoframe.geometry.unary_union
    if (union.geom_type == 'MultiPolygon'): # if there are multiple inputs, we will split a multipolygon into seperate layers
        return gpd.GeoDataFrame(geometry=list(union)).to_json()
    return gpd.GeoDataFrame(geometry=[union]).to_json()

def union_experimental(geoframe):
    differences = []
    features = np.array_split(geoframe, geoframe.size)
    for a, b in itertools.combinations(features, 2):
        print(a, b)
        difference = gpd.overlay(a, b, how='union')
        differences.append(difference)
    geoframe = gpd.GeoDataFrame(geometry=pd.concat(differences).geometry)
    print (geoframe)
    return union(geoframe)

def dissolve(geoframe):
    union = geoframe.geometry.unary_union
    return gpd.GeoDataFrame(geometry=[union]).to_json()

def intersection(geoframe):
    differences = []
    features = np.array_split(geoframe, geoframe.size)
    for a, b in itertools.combinations(features, 2):
        difference = gpd.overlay(a, b, how='intersection')
        differences.append(difference)
    geoframe = gpd.GeoDataFrame(geometry=pd.concat(differences).geometry)
    return geoframe.to_json()

def bbox(geoframe):
    geoseries = geoframe.bounds.apply(lambda row: box(row.minx, row.miny, row.maxx, row.maxy), axis=1)
    geoframe = gpd.GeoDataFrame(geometry=geoseries)
    return geoframe.to_json()

def symmetric_difference(geoframe):
    differences = []
    features = np.array_split(geoframe, geoframe.size)
    for a, b in itertools.combinations(features, 2):
        difference = gpd.overlay(a, b, how='symmetric_difference')
        differences.append(difference)
    geoframe = gpd.GeoDataFrame(geometry=pd.concat(differences).geometry)
    return geoframe.to_json()


def convert_request(json_request):
    value = -999 #standard value if no value present
    if 'value' in json_request: value = int(json_request['value'])
    geodataframe = gpd.GeoDataFrame.from_features(json_request['features'])
    geodataframe.crs = EPSG_WGS84

    return geodataframe, value

def convert_to_WGS84(geodataframe):
    return geodataframe.to_crs(EPSG_WGS84)

def convert_to_UTM_32V(geodataframe):
    return geodataframe.to_crs(EPSG_UTM32V)
