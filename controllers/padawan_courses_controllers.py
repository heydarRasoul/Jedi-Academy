from flask import jsonify, request

from db import db
from models.padawan_courses import PadawanCourses, padawan_course_schema,padawan_courses_schema
from models.padawans import Padawans
from models.courses import Courses
from util.reflection import populate_obj
from lib.authenticate import authenticate, authenticate_return_auth

@authenticate_return_auth
def enroll_padawan_in_course(auth_info):
    if auth_info.user.role =='grand-master':
        post_data = request.form if request.form else request.json
        padawan_id= post_data.get("padawan_id")
        course_id= post_data.get("course_id")

        padawan_query = db.session.query(Padawans).filter(Padawans.padawan_id == padawan_id).first()
        course_query = db.session.query(Courses).filter(Courses.course_id==course_id).first()

        if not padawan_query:
            return jsonify({"message": "padawan not found"}), 404

        if not course_query:
            return jsonify({"message":"course not found"}),404
        
        existing = db.session.query(PadawanCourses).filter_by(padawan_query=padawan_query, course_query=course_query).first()
        if existing:
            return jsonify({"message": "padawan already enrolled in course"}), 400

        new_padawan_course = PadawanCourses.new_padawan_course_obj()
        populate_obj(new_padawan_course, post_data)

        db.session.commit()
        return jsonify({"message":"hero added to quest", "result": padawan_course_schema.dump(new_padawan_course)}),200

    return jsonify({"message":"unathorized"}),400







