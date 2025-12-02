from flask import jsonify, request

from db import db
from models.temples import Temples, temple_schema, temples_schema
from models.master import Masters, master_schema,masters_schema
from models.padawans import Padawans, padawan_schema,padawans_schema
from util.reflection import populate_obj
from lib.authenticate import authenticate, authenticate_return_auth

# @authenticate_return_auth
# def create_temple(auth_info):
#     if auth_info.user.role !='grand-master':
#         return jsonify({"message":"access denied"}),403

#     post_data = request.form if request.form else request.json

#     new_temple = Temples.new_temple_obj()
#     populate_obj(new_temple, post_data)

#     try:
#         db.session.add(new_temple)
#         db.session.commit()
#     except:
#         db.session.rollback()
#         return jsonify({"message":"unable to add record"}), 400

#     return jsonify({"message":"temple added", "result": temple_schema.dump(new_temple)}), 201


def create_temple():
    

    post_data = request.form if request.form else request.json

    new_temple = Temples.new_temple_obj()
    populate_obj(new_temple, post_data)

    try:
        db.session.add(new_temple)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message":"unable to add record"}), 400

    return jsonify({"message":"temple added", "result": temple_schema.dump(new_temple)}), 201


@authenticate_return_auth
def get_temple_by_id(temple_id, auth_info):

    allowed_roles = ["master", "council-member", "grand-master"]
    if auth_info.user.role not in allowed_roles:
        return jsonify({"message": "access denied"}), 403
    
    temple_query = db.session.queery(Temples).filter(Temples.temple_id == temple_id).first()
    if not temple_query:
        return jsonify ({"message":"no result found for provided id"}),400
    else:
        return jsonify ({"message":"temple found", "result": temple_schema.dump(temple_query)}), 200

    

@authenticate_return_auth
def update_temple_by_id(temple_id, auth_info):
    if auth_info.user.role !='grand-master':
        return jsonify({"message":"access denied"}),403
    
    temple_query = db.session.query(Temples).filter(Temples.temple_id==temple_id).first()
    post_data = request.form if request.form else request.json

    if temple_query:
        populate_obj(temple_query, post_data)

        db.session.commit()

        return jsonify({"message": "temple updated", "result": temple_schema.dump(temple_query)}), 200

    return jsonify({"message": "unable to update record"}), 400


@authenticate_return_auth
def deactive_temple_by_id(temple_id, auth_info):
    if auth_info.user.role != 'grand-master':
        return jsonify({"message": "access denied"}), 403

    temple_query = db.session.query(Temples).filter(Temples.temple_id == temple_id).first()
    if not temple_query:
        return jsonify({"message": "no temple with provided id found."}), 400

    db.session.query(Padawans).filter(
        Padawans.temple_id == temple_id
    ).update({Padawans.temple_id: None})

    db.session.query(Masters).filter(
        Masters.temple_id == temple_id
    ).update({Masters.temple_id: None})

    temple_query.is_active = False

    db.session.commit()

    return jsonify({"message": "temple deactivated and members relocated"}), 200














