import json
import geopandas as gps

def buffer():
    return "hello"

def load_json(fileLocation):
    data = json.load(open(fileLocation))
    return data

def load_json_to_gps(fileLocation):
    data = gps.read_file(fileLocation)
    data_utm32N = data.to_crs(32632)
    return data_utm32N




if __name__ == "__main__":
    load_json("data/sample_data.json")
    data = load_json_to_gps("data/sample_data.json")
    data_100 = data.buffer(100)
    data_100_wgs84 = data_100.to_crs(4326)
    data_100_wgs84.to_file("countries.json", driver='GeoJSON')

