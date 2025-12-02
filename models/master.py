import uuid 
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma 

from db import db 

class Masters(db.Model):
    __tablename__ = "Masters"

    master_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Users.user_id"), nullable=False)
    master_name = db.Column(db.String(), nullable=False, unique=True)
    specialization = db.Column(db.String())
    years_training = db.Column(db.Integer())
    max_padawans = db.Column(db.Integer())

    padawans = db.relationship("Padawans", foreign_keys='[Padawans.master_id]', back_populates='master', cascade='all')
    courses = db.relationship("Courses", foreign_keys='[Courses.instructor_id]', back_populates='master', cascade='all')
    user = db.relationship("Users", foreign_keys='[Masters.user_id]', back_populates='masters')

    
    def __init__(self, user_id, master_name, specialization, years_training, max_padawans):
        self.user_id = user_id
        self.master_name = master_name
        self.specialization = specialization
        self.years_training = years_training
        self.max_padawans = max_padawans

    def new_Masters_obj():
        return Masters('','','',0,0)

class MastersSchema(ma.Schema):

    class Meta:
        fields = ['master_id','master_name', 'specialization', 'years_training', 'max_padawans', 'user', 'courses']

    master_id = ma.fields.UUID()
    master_name = ma.fields.String(required=True)
    specialization = ma.fields.String(allow_none=True)
    years_training = ma.fields.Boolean(allow_none=True)
    avg_lifespan = ma.fields.Integer(allow_none=True)
    max_padawans = ma.fields.Integer(allow_none=True)

    padawans = ma.fields.Nested("PadawansSchema", many=True, exclude=['master'])
    courses = ma.fields.Nested("CoursesSchema", many=True, exclude=['master'])
    user = ma.fields.Nested("UsersSchema")


master_schema = MastersSchema()
masters_schema = MastersSchema(many=True)