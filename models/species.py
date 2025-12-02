import uuid 
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma 

from db import db 

class Species(db.Model):
    __tablename__ = "Species"

    species_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    species_name = db.Column(db.String(), nullable=False, unique=True)
    homeworld = db.Column(db.String())
    forse_sensitive = db.Column(db.Boolean())
    avg_lifespan = db.Column(db.Integer())

    padawans = db.relationship("Padawans", foreign_keys='[Padawans.species_id]', back_populates='specie', cascade='all')

    
    def __init__(self, species_name, homeworld, forse_sensitive, avg_lifespan):
        self.species_name = species_name
        self.homeworld = homeworld
        self.forse_sensitive = forse_sensitive
        self.avg_lifespan = avg_lifespan

    def new_species_obj():
        return Species('','','','',0)

class SpeciesSchema(ma.Schema):

    class Meta:
        fields = ['species_name', 'homeworld', 'forse_sensitive', 'avg_lifespan','padawans']

    species_id = ma.fields.UUID()
    species_name = ma.fields.String(required=True)
    homeworld = ma.fields.String(allow_none=True)
    forse_sensitive = ma.fields.Boolean(allow_none=True)
    avg_lifespan = ma.fields.Integer(allow_none=True)

    padawans = ma.fields.Nested("PadawansSchema", many=True, exclude=['specie'])


specie_schema = SpeciesSchema()
species_schema = SpeciesSchema(many=True)