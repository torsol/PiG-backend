import json
import geopandas as gpd
import random
import string
import numpy as np
from shapely.geometry import box

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
    union = geoframe.geometry.unary_union
    if (union.geom_type == 'MultiPolygon'): # if there are multiple inputs, we will split a multipolygon into seperate layers
        return gpd.GeoDataFrame(geometry=list(union)).to_json()
    return gpd.GeoDataFrame(geometry=[union]).to_json()

def intersection(geoframe):
    partitions = 2
    [array1, array2] = np.array_split(geoframe, partitions)
    difference = gpd.overlay(array1, array2, how='intersection')
    return difference.to_json()

def bbox(geoframe):
    geoseries = geoframe.bounds.apply(lambda row: box(row.minx, row.miny, row.maxx, row.maxy), axis=1)
    geoframe = gpd.GeoDataFrame(geometry=geoseries)
    return geoframe.to_json()

def symmetric_difference(geoframe):
    partitions = 2
    [array1, array2] = np.array_split(geoframe, partitions)
    difference = gpd.overlay(array1, array2, how='symmetric_difference')
    return difference.to_json()


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



##################################### file specific handling ###############################################
def load_json_to_gpd(fileLocation):
    data = gpd.read_file(fileLocation)
    data.crs = EPSG_WGS84
    #data_utm32N = data.to_crs(32632)
    return data

def load_json(fileLocation):
    data = json.load(open(fileLocation))
    return data

if __name__ == "__main__":
    data = load_json_to_gpd("data/sample_union.json")
    bbox(data).to_file("union.json", driver='GeoJSON')
    #data_100_wgs84 = data_100.to_crs(4326)
    #data_100_wgs84.to_file("countries.json", driver='GeoJSON')
