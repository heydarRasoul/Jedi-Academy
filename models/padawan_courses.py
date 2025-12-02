import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db


class PadawanCourses(db.Model):
    __tablename__ = "PadawanCourses"

    padawan_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Padawans.padawan_id"), primary_key=True, default=uuid.uuid4)
    course_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Courses.course_id"), primary_key=True, default=uuid.uuid4)
    enrollment_date = db.Column(db.DateTime)
    completion_date = db.Column(db.DateTime)
    final_score = db.Column(db.Float)

    padawans = db.relationship("Padawans", back_populates="padwanCourses")
    courses = db.relationship("Courses", back_populates="padawanCourses")
  

   
    def __init__(self, padawan_id, course_id, enrollment_date=None, completion_date=None, final_score=None):
        self.padawan_id = padawan_id
        self.course_id = course_id
        self.enrollment_date = enrollment_date
        self.completion_date = completion_date
        self.final_score = final_score

    def new_padawan_course_obj():
        return PadawanCourses('','','', '', 0)


class PadawanCoursesSchema(ma.Schema):
    
    class Meta:
        fields = [ 'padawan', 'course', 'enrollment_date', 'completion_date', 'final_score']

    enrollment_date = ma.fields.DateTime()
    completion_date = ma.fields.DateTime()
    final_score = ma.fields.Float(allow_none=True)

    padawan = ma.fields.Nested("PadawansSchema")    
    course = ma.fields.Nested("CoursesSchema")
    
padawan_course_schema = PadawanCoursesSchema()
padawan_courses_schema = PadawanCoursesSchema(many=True)