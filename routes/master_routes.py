from flask import Blueprint

import controllers

masters = Blueprint('masters', __name__)

@masters.route('/master', methods=['POST'])
def create_master_route():
    return controllers.create_master()


@masters.route('/masters', methods=['GET'])
def get_all_masters_route():
    return controllers.get_all_masters()

@masters.route('/master/<master_id>', methods=['PUT'])
def update_master_by_id_route(master_id):
    return controllers.update_master_by_id(master_id)

@masters.route('/master/delete/<master_id>', methods=['DELETE'])
def delete_master_by_id_route(master_id):
    return controllers.delete_master_by_id(master_id)

 