from flask import Blueprint

import controllers

temples = Blueprint('temples', __name__)

@temples.route('/temple', methods=['POST'])
def create_temple_route():
    return controllers.create_temple()

@temples.route('/temple/<temple_id> ', methods=['GET'])
def get_temple_by_id_route(temple_id):
    return controllers.get_temple_by_id(temple_id)


@temples.route('/temple<temple_id>', methods=['PUT'])
def update_temple_by_id_route(temple_id):
    return controllers.update_temple_by_id(temple_id)



@temples.route('/temple/delete/<temple_id>', methods=['DELETE'])
def deactive_temple_by_id_route(temple_id):
    return controllers.deactive_temple_by_id(temple_id)