from flask import Blueprint

# GeoJson Geopandas(with shapely) mapbox
# Does the mapping in frontend produce WGS84?
# React, Mapbox, Turf? Material-UI?
# lat/long WGS84 = EPSG4326

blueprint = Blueprint('api', __name__)

from app.api import routes