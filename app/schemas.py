from app import app

from app.models.animals import Animal
from app.models.species import Specie
from app.models.centers import Center
from flask_marshmallow import Marshmallow

ma = Marshmallow(app)


class SpecieSchema(ma.Schema):
    class Meta:
        model = Specie
        fields = ('specie_id', 'specie_name', 'short_desc', 'price') # fields to expose

specie_schema = SpecieSchema()
species_schema = SpecieSchema(many=True)



class CenterSchema(ma.Schema):
    class Meta:
        model = Center
        fields = ('password', 'name', 'adress') # fields to expose

center_schema = CenterSchema()
centers_schema = CenterSchema(many=True)


class AnimalSchema(ma.Schema):
    class Meta:
        model = Animal
        fields = ('animal_uuid', 'name', 'age', 'short_desc', 'price', 'specie_name', 'center_id')
        # fields to expose

animal_schema = AnimalSchema()
animals_schema = AnimalSchema(many=True)