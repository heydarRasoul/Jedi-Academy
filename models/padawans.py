import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db


class Padawans(db.Model):
    __tablename__ = "Padawans"

    padawan_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    master_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Masters.master_id"), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Users.user_id"), nullable=False)
    species_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Speciess.species_id"), nullable=False)
    padawan_name = db.Column(db.String(), nullable=False, unique=True)
    age = db.Column(db.Integer())
    training_level = db.Column(db.Integer())
    graduation_date = db.Column(db.DateTime)

    user = db.relationship("Users", foreign_keys='[Padawans.padawan_id]', back_populate='padawans')
    master = db.relationship("Masters", foreign_key='[Padawans.master_id]', back_populate='padawans')
    specie = db.relationship("Species", foreign_key='[Padawans.species_id]', back_populate='padawans')
    padawanCourses = db.relationship("Padawans", back_populates='padawans', cascade='all')

   
    def __init__(self, padawan_name, age, training_level, master_id, user_id, species_id, graduation_date):
        self.padawan_name = padawan_name
        self.age = age
        self.training_level = training_level
        self.master_id = master_id
        self.user_id = user_id
        self.species_id = species_id
        self.graduation_date = graduation_date

    def new_padawan_obj():
        return Padawans('',0,0, '', '', '','')


class PadawansSchema(ma.Schema):
    
    class Meta:
        fields = [ 'padawan_id','padawan_name', 'age', 'training_level', 'master_id', 'user_id', 'specie', 'graduation_date']

    padawan_id = ma.fields.UUID()
    padawan_name = ma.fields.String(required=True)
    age = ma.fields.Integer(allow_none=True)
    training_level = ma.fields.Integer(allow_none=True)
    graduation = ma.fields.DateTime()

    master = ma.fields.Nested("MastersSchema")    
    specie = ma.fields.Nested("SpeciesSchema")
    user = ma.fields.Nested("UsersSchema")
    
padawan_schema = PadawansSchema()
padawans_schema = PadawansSchema(many=True)