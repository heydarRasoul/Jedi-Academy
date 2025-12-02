from flask import jsonify, request

from db import db
from models.master import Masters, master_schema, masters_schema
from util.reflection import populate_obj
from lib.authenticate import authenticate, authenticate_return_auth

@authenticate_return_auth
def create_master(auth_info):
    post_data = request.form if request.form else request.json

    if auth_info.user.role =='grand-master':
        new_master = Masters.new_master_obj()
        populate_obj(new_master, post_data)

        try:
            db.session.add(new_master)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message":"unable to add record"}), 400

        return jsonify({"message":"user added", "result": master_schema.dump(new_master)}), 201
    
    return jsonify({"message":"unathorized"}),400

@authenticate_return_auth
def get_all_masters(auth_info):
    allowed_roles = ['grand-master','master','council-member','padawan','knight']
    if auth_info.user.role not in allowed_roles:
        return jsonify({"message":"access denied"}),400
    
    masters_query = db.session.query(Masters).all()
    if not masters_query:
        return jsonify({"message": "masters not founded."}),400

    return jsonify({"message":"masters found", "results":masters_schema.dump(masters_query)}),200

@authenticate_return_auth
def update_master(master_id, auth_info):
    allowed_roles = ['grand-master','council-member']

    if auth_info.user.role not in allowed_roles:
        if auth_info.user.role == 'master' and auth_info.user.master_id == master_id:
            pass
        return jsonify({"message":"access denied"}),400
    
    post_data = request.form if request.form else request.json

    master_query = db.session.query(Masters).filter(Masters.master_id== master_id).first()
    if master_query:
        populate_obj(master_query, post_data)
        db.session.commit()

        return jsonify({"message":"record updated","result": master_schema.dump(master_query)}),200

    return jsonify({"message": "unable to update record"}), 400



@authenticate_return_auth
def delete_padawan_by_id(master_id, auth_info):
    master_query = db.session.query(Masters).filter(Masters.master_id == master_id).first()

    if auth_info.user.role == 'grand-master':
        if not master_query:
            return jsonify({"message": "no master with provided id founded."}),400
    
        db.session.delete(master_query)
        db.session.commit()

        return jsonify({"message":"master deleted"}),200
    
    return jsonify({"message":"unathorized"}),400
    
