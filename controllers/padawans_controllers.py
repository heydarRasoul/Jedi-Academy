from flask import jsonify, request

from db import db
from models.padawans import Padawans, padawan_schema, padawans_schema
from models.users import Users, user_schema, users_schema
from util.reflection import populate_obj
from lib.authenticate import authenticate, authenticate_return_auth


@authenticate_return_auth
def create_padawan(auth_info):
    post_data = request.form if request.form else request.json

    if auth_info.user.role =='grand-master' or auth_info.user.role == 'master':
        new_padawan = Padawans.new_padawan_obj()
        populate_obj(new_padawan, post_data)

        try:
            db.session.add(new_padawan)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message":"unable to add record"}), 400

        return jsonify({"message":"padawan added", "result": padawan_schema.dump(new_padawan)}), 201
    
    return jsonify({"message":"unathorized"}),400


@authenticate_return_auth
def get_all_padawans(auth_info):
    
    padawans_query = db.session.query(Padawans).all()
    if auth_info.user.role =='grand-master' or auth_info.user.role == 'master' or auth_info.user.role =='council-member':
        if not padawans_query:
            return jsonify({"message": "padawans not founded."}),400

        return jsonify({"message":"padawans found", "results":padawans_schema.dump(padawans_query)}),200

    return jsonify({"message":"access denied"}),400

    
@authenticate_return_auth
def get_active_padawans(auth_info):
    active_padawans_query = db.session.query(Padawans).filter(Padawans.	
        graduation_date.is_(None)).all()

    if auth_info.user.role =='grand-master' or auth_info.user.role == 'master' or auth_info.user.role =='council-member':
        if not active_padawans_query:
            return jsonify({"message": "no active padawans found"}), 404
    
        return jsonify({"message":"padawan found", "result": padawans_schema.dump(active_padawans_query)}), 200
    
    return jsonify({"message":"access denied"}),403


@authenticate_return_auth
def update_padawan_by_id(padawan_id, auth_info):

    allowed_roles = ['grand-master','council-member']

    if auth_info.user.role not in allowed_roles:
        if auth_info.user.role == 'master' and auth_info.user.padawan_id == padawan_id:
            pass
        return jsonify({"message":"access denied"}),400
    

    post_data = request.form if request.form else request.json

    padawan_query = db.session.query(Padawans).filter(Padawans.padawan_id == padawan_id).first()
    
    if not padawan_query:
        return jsonify({"message": "padawan not found"}), 404
    
    else:
        populate_obj(padawan_query, post_data)
        db.session.commit()

        return jsonify({"message": "padawan found", "result": padawan_schema.dump(padawan_query)}), 200


@authenticate_return_auth
def promote_padawan_to_knight(padawan_id, auth_info):

    allowed_roles = ['grand-master','council-member']

    if auth_info.user.role not in allowed_roles:
        return jsonify({"message":"access denied"}),400
    

    post_data = request.form if request.form else request.json

    padawan_query = db.session.query(Padawans).filter(Padawans.padawan_id == padawan_id).first()
    if not padawan_query:
        return jsonify({"message": "padawan not found"}), 404
    
    user_query = db.session.query(Users).filter(Users.user_id == padawan_query.user_id).first()
    
    if not user_query:
        return jsonify({"message": "user linked to padawan not found"}), 400

    
    updated_user = Users.new_user_obj()
    populate_obj(updated_user, post_data.force_rank)

    update_padawan = Padawans.new_padawan_obj()
    populate_obj(update_padawan, post_data.graduation_date)
   
        
    db.session.commit()

    return jsonify({"message": "padawan found", "result": padawan_schema.dump(padawan_query)}), 200



@authenticate_return_auth
def delete_padawan_by_id(padawan_id, auth_info):
    padawan_query = db.session.query(Padawans).filter(Padawans.padawan_id == padawan_id).first()

    if auth_info.user.role == 'grand-master':
        if not padawan_query:
            return jsonify({"message": "no padwan with provided id founded."}),400
    
        db.session.delete(padawan_query)
        db.session.commit()

        return jsonify({"message":"padawan deleted"}),200
    
    return jsonify({"message":"unathorized"}),400
    


