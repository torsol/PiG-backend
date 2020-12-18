import json
import geopandas as gpd
import random
import string
import numpy as np
from shapely.geometry import box
import itertools
import pandas as pd

# EPSG codes relevant for the projection of the buffer
EPSG_WGS84 = 'EPSG:4326'
EPSG_UTM32N = 'EPSG:32632'

def clean_response(json_response):
    '''clean response takes the json created in the functions and removes the clutter created by geopandas'''
    if('bbox' in json_response): del json_response['bbox']
    if('bbox' in json_response['features'][0]): 
        for i in range(0, len(json_response['features'])):
            del json_response['features'][i]['bbox'] # assumes only one feature in the collection
    return json_response


def buffer(geoframe, value):
    '''buffer creates a buffer around all the geometries in the geoframe, using the value'''
    # convert to UTM32 for reference system in meters
    data_utm32V = convert_to_UTM_32V(geoframe)

    # apply buffer
    data_utm32V_buffer = data_utm32V.buffer(value)

    # convert back to WGS84
    data_wgs84_buffer = convert_to_WGS84(data_utm32V_buffer)

    data_wgs84_buffer_json = json.loads(data_wgs84_buffer.to_json())

    return clean_response(data_wgs84_buffer_json)

def union(geoframe):
    '''union uses geopandas.unary_union to create the unified layer'''
    union = geoframe.geometry.unary_union
    if (union.geom_type == 'MultiPolygon'): # if there are multiple inputs, we will split a multipolygon into seperate layers
        return gpd.GeoDataFrame(geometry=list(union)).to_json()
    return gpd.GeoDataFrame(geometry=[union]).to_json()

def dissolve(geoframe):
    '''dissolve uses the same unary union, without splitting the resultant multi-polygon'''
    union = geoframe.geometry.unary_union
    return gpd.GeoDataFrame(geometry=[union]).to_json()

def intersection(geoframe):
    '''intersection takes the pairwise combination of features from the two layers, by the geopandas overlay function'''
    differences = []
    features = np.array_split(geoframe, geoframe.size)
    for a, b in itertools.combinations(features, 2):
        difference = gpd.overlay(a, b, how='intersection')
        differences.append(difference)
    geoframe = gpd.GeoDataFrame(geometry=pd.concat(differences).geometry)
    return geoframe.to_json()

def bbox(geoframe):
    '''Bounding box is created by using the geopandas.bounds method of each feature in the dataframe'''
    geoseries = geoframe.bounds.apply(lambda row: box(row.minx, row.miny, row.maxx, row.maxy), axis=1)
    geoframe = gpd.GeoDataFrame(geometry=geoseries)
    return geoframe.to_json()

def symmetric_difference(geoframe):
    '''symmetric difference takes the pairwise combination of features from the two layers, by the geopandas overlay function'''
    differences = []
    features = np.array_split(geoframe, geoframe.size)
    for a, b in itertools.combinations(features, 2):
        difference = gpd.overlay(a, b, how='symmetric_difference')
        differences.append(difference)
    geoframe = gpd.GeoDataFrame(geometry=pd.concat(differences).geometry)
    return geoframe.to_json()


def convert_request(json_request):
    '''convert request transfers the raw input from the HTTP-request into a readible format for the API'''
    value = -999 #standard value if no value present
    if 'value' in json_request: value = int(json_request['value'])
    geodataframe = gpd.GeoDataFrame.from_features(json_request['features'])
    geodataframe.crs = EPSG_WGS84

    return geodataframe, value

def convert_to_WGS84(geodataframe):
    return geodataframe.to_crs(EPSG_WGS84)

def convert_to_UTM_32V(geodataframe):
    return geodataframe.to_crs(EPSG_UTM32N)
