from flask import jsonify, request

from db import db
from models.lightsabers import Lightsabers, lightsaber_schema, lightsabers_schema
from util.reflection import populate_obj
from lib.authenticate import authenticate, authenticate_return_auth


@authenticate_return_auth
def create_lightsaber(auth_info):
    post_data = request.form if request.form else request.json

    if auth_info.user.role =='grand-master' or auth_info.user.role == 'padawan':
        new_lightsaber = Lightsabers.new_lightsaber_obj()
        populate_obj(new_lightsaber, post_data)

        try:
            db.session.add(new_lightsaber)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message":"unable to add record"}), 400

        return jsonify({"message":"lightsaber added", "result": lightsaber_schema.dump(new_lightsaber)}), 201
    
    return jsonify({"message":"unathorized"}),400


@authenticate_return_auth
def get_lightsaber_by_id(owner_id, auth_info):
    if auth_info.user.user_id != owner_id:
        return jsonify({"message":"access denied"}),403

    lightsaber_query = db.session.query(Lightsabers).filter(Lightsabers.owner_id == owner_id).first()
    if lightsaber_query:
        return jsonify ({"mesage":"lightsaber founded","result": lightsaber_schema.dump(lightsaber_query)})

    return jsonify({"message":"lightsaber not found."}), 400



@authenticate_return_auth
def update_lightsaber_by_id(saber_id, auth_info):
    post_data = request.form if request.form else request.json  
     
    saber_query =db.session.query(Lightsabers).filter(Lightsabers.saber_id == saber_id).first() 
    if not saber_query:
        return jsonify({"message": "lightsaber not found"}), 404

    owner_id = saber_query.owner_id
    if auth_info.user.user_id != owner_id:
        return jsonify({"message":"access denied"}),403
    
    populate_obj(saber_query, post_data)
    db.session.commit()

    return jsonify({"message":"record updated","result": lightsaber_schema.dump(saber_query)}),200

    

@authenticate_return_auth
def delete_lightsaber_by_id(saber_id, auth_info):
    post_data = request.form if request.form else request.json  
     
    saber_query =db.session.query(Lightsabers).filter(Lightsabers.saber_id == saber_id).first() 
    if not saber_query:
        return jsonify({"message": "lightsaber not found"}), 404

    owner_id = saber_query.owner_id
    allowed_roles = ['grand-master','council-member']

    if auth_info.user.role not in allowed_roles:
        if auth_info.user.user_id == owner_id:
            pass
        return jsonify({"message":"access denied"}),400
    
    db.session.delete(saber_query)
    db.session.commit()

    return jsonify({"message":"lightsaber deleted"}),200
    
    
    








