from flask import jsonify

from app import db
import datetime, enum
from other_methods import generate_uuid
from app.models.animals import get_by_center_id, Animal


# enum choice class for is_published field in book model


class Center(db.Model):
    __tablename__ = "center"

    center_id = db.Column(db.String(255), nullable=False, unique = True, primary_key=True)
    password = db.Column(db.String(32), nullable = False)
    name = db.Column(db.String(100), nullable=False, unique = True)
    adress = db.Column(db.Text(), nullable = False)
    animals = db.relationship(Animal, backref='center', lazy=True)

    def __init__(self, center_id, password, name, adress):
        self.center_id = center_id
        self.password = password
        self.name = name
        self.adress = adress

    def center_info_json(self):
        return {'id': self.center_id, 'name': self.name, 'adress': self.adress}



# przeniesc do routes
def get_centers():
    return {'centers': [center.center_info_json for center in Center.query.all()]}

def get_center_by_id(center_id):
    center = Center.query.filter_by(center_id=center_id).first()
    animals = get_by_center_id(center_id)
    return jsonify({'center info': center, 'animals': animals})