from flask import jsonify, request

from db import db
from models.crystals import Crystals, crystal_schema, crystals_schema
from util.reflection import populate_obj
from lib.authenticate import authenticate, authenticate_return_auth

@authenticate_return_auth
def create_crystal(auth_info):
    post_data = request.form if request.form else request.json

    if auth_info.user.role =='grand-master' or auth_info.user.role == 'master':
        new_crystal= Crystals.new_crystal_obj()
        populate_obj(new_crystal, post_data)

        try:
            db.session.add(new_crystal)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message":"unable to add record"}), 400

        return jsonify({"message":"crystal added", "result": crystal_schema.dump(new_crystal)}), 201
    
    return jsonify({"message":"unathorized"}),400


    
@authenticate_return_auth
def get_crystal_by_rarity(rarity_level, auth_info):
    crystal_query = db.session.query(Crystals).filter(Crystals.rarity_level == rarity_level).all()

    if auth_info.user.role =='grand-master' or auth_info.user.role == 'master':
        if not crystal_query:
            return jsonify({"message": "no crystal found"}), 404
    
        return jsonify({"message":"crystal found", "result": crystal_schema.dump(crystal_query)}), 200
    
    return jsonify({"message":"access denied"}),403