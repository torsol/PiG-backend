from app.api import blueprint
from flask import request

from app.api.operations.operations import buffer
from app.api.operations.operations import union
from app.api.operations.operations import convert_request

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