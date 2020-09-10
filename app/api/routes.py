from app.api import blueprint
from flask import request

from app.api.operations.buffer import buffer
from app.api.operations.buffer import convert_request

@blueprint.route('/users', methods=['GET'])
def get_users():
    return "test"

@blueprint.route('/buffer', methods=['POST'])
def compute_buffer():
    request_json = request.get_json()
    geoframe, value = convert_request(request_json)
    return buffer(geoframe, value)