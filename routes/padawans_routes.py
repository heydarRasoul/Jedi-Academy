from flask import Blueprint

import controllers

padawans = Blueprint('padawans', __name__)

@padawans.route('/padawan', methods=['POST'])
def create_padawan_route():
    return controllers.create_padawan()

@padawans.route('/padawans', methods=['GET'])
def get_all_padawans_route():
    return controllers.get_all_padawans()


@padawans.route('/padawans/active', methods=['GET'])
def get_active_padawans_route():
    return controllers.get_active_padawans()


@padawans.route('/padawan/<padawan_id>', methods=['PUT'])
def update_padawan_by_id_route(padawan_id):
    return controllers.update_padawan_by_id(padawan_id)

@padawans.route('/padawan/<padawan_id>/promote', methods=['PUT'])
def promote_padawan_to_knight_route(padawan_id):
    return controllers.promote_padawan_to_knight(padawan_id)

@padawans.route('/padawan/delete/<padawan_id>', methods=['DELETE'])
def delete_padawan_by_id_route(padawan_id):
    return controllers.delete_padawan_by_id(padawan_id)