from flask import jsonify

from app import db
from sqlalchemy_utils import ChoiceType
from app.models.animals import Animal, get_by_specie_name
import datetime, enum
from other_methods import generate_uuid



class Specie(db.Model):
    __tablename__ = "species"

    specie_id = db.Column(db.Integer, nullable=False, primary_key=True, unique=True, default=generate_uuid())
    specie_name = db.Column(db.String(100), nullable=False, unique=True)
    short_desc = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)

    created = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), nullable=False)

    animals = db.relationship(Animal, backref='specie', lazy=True)

    def __init__(self, specie_id, specie_name, short_desc, price):
        self.specie_id = specie_id
        self.specie_name = specie_name
        self.short_desc = short_desc
        self.price = price

    def specie_info_json(self):
        return {'id': self.specie_id, 'name': self.specie_name, 'description': self.short_desc, 'price': self.price}

# przeniesc do routes
def specie_by_name(specie_name):
    specie = Specie.query.filter_by(specie_name=specie_name).first()
    animals = get_by_specie_name(specie_name)
    return jsonify({'specie info': specie.specie_info_json(), 'animals': animals})