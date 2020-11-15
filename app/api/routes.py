from app.api import blueprint
from flask import request

from app.api.operations.operations import buffer
from app.api.operations.operations import dissolve
from app.api.operations.operations import symmetric_difference
from app.api.operations.operations import bbox
from app.api.operations.operations import union
from app.api.operations.operations import intersection
from app.api.operations.operations import convert_request

@blueprint.route('/ping', methods=['GET'])
def ping():
    return "pong"

@blueprint.route('/buffer', methods=['POST'])
def compute_buffer():
    request_json = request.get_json()
    geoframe, value = convert_request(request_json)
    return buffer(geoframe, value)

@blueprint.route('/union', methods=['POST'])
def compute_union():
    request_json = request.get_json()
    geoframe, _ = convert_request(request_json)
    return union(geoframe)

@blueprint.route('/intersection', methods=['POST'])
def compute_intersection():
    request_json = request.get_json()
    geoframe, _ = convert_request(request_json)
    return intersection(geoframe)

@blueprint.route('/bbox', methods=['POST'])
def compute_bbox():
    request_json = request.get_json()
    geoframe, _ = convert_request(request_json)
    return bbox(geoframe)

@blueprint.route('/symmetric_difference', methods=['POST'])
def compute_symmetric_difference():
    request_json = request.get_json()
    geoframe, _ = convert_request(request_json)
    return symmetric_difference(geoframe)

@blueprint.route('/dissolve', methods=['POST'])
def compute_dissolve():
    request_json = request.get_json()
    geoframe, _ = convert_request(request_json)
    return dissolve(geoframe)