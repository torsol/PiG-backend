from app.api import blueprint

@blueprint.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    pass

@blueprint.route('/users', methods=['GET'])
def get_users():
    return "test"

@blueprint.route('/users/<int:id>/followers', methods=['GET'])
def get_followers(id):
    pass

@blueprint.route('/users/<int:id>/followed', methods=['GET'])
def get_followed(id):
    pass

@blueprint.route('/users', methods=['POST'])
def create_user():
    pass

@blueprint.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    pass