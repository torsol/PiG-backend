from app.api import blueprint

@blueprint.route('/users', methods=['GET'])
def get_users():
    return "test"

@blueprint.route('/buffer', methods=['GET'])
def compute_buffer():
    return "buffer"