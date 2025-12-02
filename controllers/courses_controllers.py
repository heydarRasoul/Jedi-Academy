from flask import jsonify, request

from db import db
from models.courses import Courses, courses_schema, course_schema
from models.padawan_courses import PadawanCourses, padawan_course_schema
from util.reflection import populate_obj
from lib.authenticate import authenticate, authenticate_return_auth


@authenticate_return_auth
def create_course(auth_info):
    post_data = request.form if request.form else request.json

    if auth_info.user.role =='grand-master' or auth_info.user.role == 'master':
        new_course = Courses.new_course_obj()
        populate_obj(new_course, post_data)

        try:
            db.session.add(new_course)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message":"unable to add record"}), 400

        return jsonify({"message":"course added", "result": course_schema.dump(new_course)}), 201
    
    return jsonify({"message":"unathorized"}),400

@authenticate
def get_courses_by_difficulty_level(difficulty_level):
    courses_query = db.session.query(Courses).filter(Courses.difficulty_level == difficulty_level).all()

  
    if not courses_query:
        return jsonify({"message": "no course found"}), 404

    return jsonify({"message":"crystal found", "result": courses_schema.dump(courses_query)}), 200
    

@authenticate_return_auth
def update_course_by_id(course_id, auth_info):

    allowed_roles = ['grand-master','council-member', 'master']

    if auth_info.user.role not in allowed_roles:
        return jsonify({"message":"access denied"}),400
    

    post_data = request.form if request.form else request.json

    course_query = db.session.query(Courses).filter(Courses.course_id == course_id).first()
    
    if not course_query:
        return jsonify({"message": "course not found"}), 404
    
    else:
        populate_obj(course_query, post_data)
        db.session.commit()

        return jsonify({"message": "course found", "result": course_schema.dump(course_query)}), 200
        



@authenticate_return_auth
def delete_course_by_id(course_id, auth_info):
    course_query = db.session.query(Courses).filter(Courses.course_id == course_id).first()

    if auth_info.user.role == 'grand-master':
        if not course_query:
            return jsonify({"message": "no padwan with provided id founded."}),400

        db.session.query(PadawanCourses).filter(PadawanCourses.course_id == course_id
        ).delete()

        db.session.delete(course_query)
        db.session.commit()

        return jsonify({"message":"course deleted"}),200
    
    return jsonify({"message":"unathorized"}),400
    


