from app import app, db

from app.models.animals import Animal
from app.models.centers import Center
from app.models.species import Specie
from sqlalchemy import select
from app.schemas import center_schema, centers_schema, animal_schema, animals_schema, specie_schema, species_schema

import argparse
import logging
from app.engine import engine
from sqlalchemy import select
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from sqlalchemy import text

from flask import request, jsonify, make_response


jwt = JWTManager(app)


@app.route("/add_specie", methods=["POST"])
@jwt_required()
def add_specie(specie_id):
    parser = argparse.ArgumentParser()  # only allow price changes, no name changes allowed
    parser.add_argument('specie_name', type=str, required=True, default="NoName",
                        help="string type, this field cannot be left blank, default = NoName")
    parser.add_argument('short_desc', type=str, required=True, default="None",
                        help="Must enter the specie name (type = str), default = None"
                        )
    parser.add_argument('price', type=float, required=True, default=0.0,
                        help="This field can be left blank (type = float), default = 0.0")
    args = parser.parse_args()

    specie_nam = args.specie_name
    specie_name = specie_nam.lower()
    short_desc = args.short_desc
    price = args.price

    if Specie.query.filer_by(specie_name=specie_name).first():
        logging.error('Specie is already exist')
    else:
        new_specie = Specie(specie_id, specie_name, short_desc, price)

        db.session.add(new_specie)
        db.session.commit()

        result = specie_schema.dump(new_specie)

        data = {
            'message': 'New Specie Created!',
            'status': 201,
            'data': result
        }
        logging.debug(data)


# endpoint to GET all categories
@app.route("/species", methods=["GET"])
def get_species():
    all_species = Specie.query.all()
    result = species_schema.dump(all_species)
    all_species_names = Specie.query.with_entities(Specie.specie_name)
    for specie in all_species_names:
        count = Animal.query.filter_by(specie_name=specie).count()
        data_specie = {
            'specie': result,
            'num_of_animals': count
        }
        print(jsonify(data_specie))
    return logging.debug("species printed")


# endpoint to GET category detail by id
@app.route("/specie/<int:specie_id>", methods=["GET"])
def get_specie(specie_id):
    specie = Specie.query.get(specie_id)
    animals = [animal.animal_info_json_simpl for animal in Animal.query.filter_by(specie_id=specie_id).all()]

    if (specie):
        result = specie_schema.dump(specie)
        data = {
            'message': 'Specie Info!',
            'status': 200,
            'data': result,
            'animals': animals
        }
        logging.debug('specie', specie_id, 'printed')
    else:
        data = {
            'message': 'Invalid Specie ID!',
            'status': 200
        }
        logging.error('Invalid Specie ID')
    return make_response(jsonify(data))