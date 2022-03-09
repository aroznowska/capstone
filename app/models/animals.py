from app import db
import datetime, enum
from other_methods import generate_uuid
from flask.json import jsonify


class Animal(db.Model):
    __tablename__ = "animals"

    animal_uuid = db.Column(db.String(255), nullable=False, unique=True, default=generate_uuid(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.DateTime(), nullable=False) #age -->Birth Date
    short_desc = db.Column(db.Text(), default = None)
    price = db.Column(db.Float, default = None)

    specie_name = db.Column(db.Integer, db.ForeignKey("specie.specie_name"), nullable=False)
    center_id = db.Column(db.Integer, db.ForeignKey("center.center_id"), nullable=False)

    created = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), nullable=False)
    modified = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(),
                         onupdate=db.func.current_timestamp(), nullable=False)

    def __init__(self, animal_uuid, name, age, short_desc, price, specie_name, center_id):
        self.animal_uuid = animal_uuid
        self.name = name
        self.age = age
        self.short_desc = short_desc
        self.price = price
        self.specie_name = specie_name
        self.center_id = center_id

    @classmethod
    def get_by_id(cls, animal_uuid):
        animal=cls.query.filter_by(animal_uuid=animal_uuid).first()
        return jsonify(animal)

    def animal_info_json(self):
        return {'id': self.animal_uuid, 'name': self.name, 'specie': self.specie_name, 'center_id': self.center_id,
               'Birth_Date' : self.age, 'description': self.short_desc, 'price': self.price}

    def animal_info_json_simpl(self):
        return {'id': self.animal_uuid, 'name': self.name, 'specie': self.specie_name}

    # def animal_to_history(self):
    #     # czy na pewno tak?
    #     animal = {'time': self.created, 'time_mod': self.modified, 'id': self.animal_uuid, 'name': self.name,
    #               'specie': self.specie_name, 'center_id': self.center_id,
    #               'Birth_Date' : self.age, 'description': self.short_desc, 'price': self.price}
    #     return animal

    @classmethod
    def animal_count(cls, specie_name):
        return cls.query.filter_by(specie_name=specie_name).count()


    def get_animal_list(self):
        return {'animals': [animal.animal_info_json for animal in Animal.query.all()]}

    @classmethod
    def get_by_specie_name(cls, specie_name):
        animals = [animal.animal_info_json for animal in cls.query.filter_by(specie_name=specie_name).all()]
        return animals

    @classmethod
    def get_by_center_id (cls, center_id):
        animals = [animal.animal_info_json for animal in cls.query.filter_by(center_id=center_id).all()]
        return animals