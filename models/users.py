import marshmallow as ma 
import uuid
from sqlalchemy.dialects.postgresql import UUID 

from db import db

class Users(db.Model):
    __tablename__ = "Users"

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    temple_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Temples.temple_id"), nullable=False)
    username = db.Column(db.String(),nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False, unique=True)   
    password = db.Column(db.String(), nullable=False)
    force_rank = db.Column(db.String())
    midi_count = db.Column(db.Integer())
    is_active = db.Column(db.Boolean(), default=True)
    join_date = db.Column(db.DateTime)

   
    auth = db.relationship("AuthTokens",back_populates="user")
    masters =db.relationship("Masters", foreign_keys='[Masters.user_id]', back_populates='user', cascade='all')
    padawans =db.relationship("Padawans", foreign_keys='[Padawans.user_id]', back_populates='user', cascade='all')
    lightsabers =db.relationship("Lightsabers", foreign_keys='[Lightsabers.owner_id]', back_populates='user', cascade='all')
    temple= db.relationship("Temples", foreign_keys='[Users.temple_id]', back_populates='users')

    def __init__(self, temple_id, username, email, password, force_rank, midi_count, join_date, is_active=True):
        self.temple_id = temple_id
        self.username = username
        self.email = email
        self.password = password
        self.force_rank = force_rank
        self.midi_count = midi_count
        self.join_date = join_date
        self.is_active = is_active
       


    def new_user_obj():
        return Users('','','','','','','',True)
    

class UsersSchema(ma.Schema):
    class Meta:
        fields = [ 'user_id','temple', 'username', 'email', 'force_rank', 'midi_count', 'join_date', 'is_active', 'masters']


    user_id = ma.fields.UUID()
    username = ma.fields.String(required=True)
    email= ma.fields.String(required=True)
    force_rank = ma.fields.String(allow_none=True)
    midi_count = ma.fields.Integer()
    is_active = ma.fields.Boolean(allow_none=True, dump_default=True)
    join_date = ma.fields.DateTime()

    temple= ma.fields.Nested("TemplesSchema")
    masters = ma.fields.Nested("MastersSchema")
    lightsabers = ma.fields.Nested("LightsabersSchema")
    padawans = ma.fields.Nested("PadawansSchema")

user_schema = UsersSchema()
users_schema = UsersSchema(many=True)