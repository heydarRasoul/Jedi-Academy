
from flask import jsonify, request

from db import db
from models.species import Species, SpeciesSchema, specie_schema
from util.reflection import populate_obj
from lib.authenticate import authenticate, authenticate_return_auth


@authenticate_return_auth
def create_species(auth_info):
    post_data = request.form if request.form else request.json

    if auth_info.user.role =='grand-master' or auth_info.user.role == 'master':
        new_species = Species.new_species_obj()
        populate_obj(new_species, post_data)

        try:
            db.session.add(new_species)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message":"unable to add record"}), 400

        return jsonify({"message":"species added", "result": specie_schema.dump(new_species)}), 201
    
    return jsonify({"message":"unathorized"}),400

   
@authenticate
def get_species_by_id(species_id):
    species_query = db.session.query(Species).filter(Species.species_id == species_id).first()

    
    if not species_query:
        return jsonify({"message": "species not found"}), 404
    
    return jsonify({"message":"species found", "result": specie_schema.dump(species_query)}), 200
    
   
