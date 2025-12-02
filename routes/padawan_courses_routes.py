from flask import Blueprint

import controllers

padawan_course = Blueprint('padawan_course', __name__)

@padawan_course.route('/enrollment', methods=['POST'])
def enroll_padawan_in_course_route():
    return controllers.enroll_padawan_in_course()