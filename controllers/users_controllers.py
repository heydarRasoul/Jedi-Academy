from flask import jsonify, request

from flask_bcrypt import generate_password_hash

from db import db
from models.users import Users, user_schema, users_schema
from util.reflection import populate_obj
from lib.authenticate import authenticate, authenticate_return_auth


def create_user():
    post_data = request.form if request.form else request.json
    
    new_user = Users.new_user_obj()
    populate_obj(new_user, post_data)

    new_user.password = generate_password_hash(new_user.password).decode('utf-8')

    try:
        db.session.add(new_user)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message":"unable to add record"}), 400

    return jsonify({"message":"user added", "result": user_schema.dump(new_user)}), 201

    


@authenticate_return_auth
def get_all_users(auth_info):
    
    users_query = db.session.query(Users).all()
    if auth_info.user.role =='council-member' or auth_info.user.role == 'grand-master':
        if not users_query:
            return jsonify({"message": "users not founded."}),400

        return jsonify({"message":"users found", "results":users_schema.dump(users_query)}),200

    return jsonify({"message":"unathorized"}),400


    
@authenticate_return_auth
def get_user_profile(user_id,auth_info):
    user_query = db.session.query(Users).filter(Users.user_id==auth_info.user_id).first()

    if user_id==str(auth_info.user.user_id):
        if not user_query:
            return jsonify({"message": "User not found"}), 404
    
    return jsonify({"message":"user found", "result": user_schema.dump(user_query)}), 200
    
   

@authenticate_return_auth
def update_user_by_id(user_id, auth_info):
    user_query = db.session.query(Users).filter(Users.user_id==user_id).first()
    post_data = request.form if request.form else request.json

    if auth_info.user.role =='council-member' or auth_info.user.role == 'grand-master' or user_id==str(auth_info.user.user_id):
        populate_obj(user_query, post_data)

        db.session.commit()
   
        return jsonify({"message": "user found", "result": user_schema.dump(user_query)}), 200
    
    return jsonify({"message": "unable to update record"}), 400



@authenticate_return_auth
def delete_user_by_id(user_id, auth_info):
    user_query = db.session.query(Users).filter(Users.user_id==user_id).first()

    if auth_info.user.role == 'grand-master':
        if not user_query:
            return jsonify({"message": "no user with provided id founded."}),400
    
        db.session.delete(user_query)
        db.session.commit()

        return jsonify({"message":"user deleted"}),200
    
    return jsonify({"message":"unathorized"}),400
    



