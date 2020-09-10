import json
import geopandas as gpd

EPSG_WGS84 = 'EPSG:4326'
EPSG_UTM32V = 'EPSG:32632'


def buffer(geoframe, value):
    # convert to UTM32 for reference system in meters
    data_utm32V = convert_to_UTM_32V(geoframe)

    # apply buffer
    data_utm32V_buffer = data_utm32V.buffer(value)

    # convert back to WGS84
    data_wgs84_buffer = convert_to_WGS84(data_utm32V_buffer)

    return data_wgs84_buffer.to_json()

def convert_request(json_request):
    value = int(json_request['value'])
    geodataframe = gpd.GeoDataFrame.from_features(json_request['layers']['features'])
    geodataframe.crs = EPSG_WGS84

    return geodataframe, value

def convert_to_WGS84(geodataframe):
    return geodataframe.to_crs(EPSG_WGS84)

def convert_to_UTM_32V(geodataframe):
    return geodataframe.to_crs(EPSG_UTM32V)



##################################### file specific handling ###############################################
def load_json_to_gps(fileLocation):
    data = gpd.read_file(fileLocation)
    data_utm32N = data.to_crs(32632)
    return data_utm32N

def load_json(fileLocation):
    data = json.load(open(fileLocation))
    return data

if __name__ == "__main__":
    load_json("data/sample_data.json")
    data = load_json_to_gps("data/sample_data.json")
    data_100 = data.buffer(100)
    data_100_wgs84 = data_100.to_crs(4326)
    data_100_wgs84.to_file("countries.json", driver='GeoJSON')
