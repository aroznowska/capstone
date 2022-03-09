from app import app, db

from app.models.animals import Animal
from app.models.centers import Center
from app.models.species import Specie
from app.schemas import center_schema, centers_schema, animal_schema, animals_schema, specie_schema, species_schema

import argparse
import logging

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_restful import reqparse, abort, Api, Resource
from flask import request, jsonify, make_response


jwt = JWTManager(app)


@app.route("/animal", methods=["POST"])
@jwt_required()
def add_animal():
    animal_name = request.json['animal_name']
    birth_date = request.json['birth_date']
    description = request.json['description']
    price = request.json['price']
    specie_nam=request.json['specie_nam']

    specie_name = specie_nam.lower()

    if Specie.query.filer_by(specie_name=specie_name).first():
        logging.error('Specie is already exist')
    else:

        new_specie = Specie(specie_name, description, price)
        db.session.add(new_specie)
        db.session.commit()

        result = specie_schema.dump(new_specie)

    if Specie.query.filter_by(specie_name=specie_name).one_or_none():
        center_id = get_jwt_identity()
        new_animal = Animal(animal_name, birth_date, description, price, specie_name,
                            center_id)

        db.session.add(new_animal)
        db.session.commit()

        result = animal_schema.dump(new_animal)

        data = {
            'message': 'New Animal Added!',
            'status': 201,
            'data': result
            }
        return make_response(jsonify(data)), logging.debug("Animal added")
    else:
        return logging.error("Specie doesn't exist")


@app.route("/animals", methods=["GET"])
def get_all_animals():
    all_animals = Animal.query.all()
    result = animals_schema.dump(all_animals)

    data = {
        'message': 'All Animals!',
        'status': 200,
        'data': result
    }
    return make_response(jsonify(data)), logging.debug("List of all Animals", result)


@app.route("/animal/<path:animal_uuid>", methods=["GET"])
def get_animal(animal_uuid):
    animal = Animal.query.get(animal_uuid)

    if (animal):
        result = animal_schema.dump(animal)
        data = {
            'message': 'Animal Info!',
            'status': 200,
            'data': result
        }
        return logging.debug("animal info"), make_response(jsonify(data))
    else:
        data = {
            'message': 'Invalid Book ID!',
            'status': 200
        }
        return logging.error("Invalid animal id")


@app.route("/animal_update/<path:animal_uuid>", methods=["PUT"])
@jwt_required()
def update_animal():
    animal_uuid = request.json['animal_uuid']
    animal_name = request.json['animal_name']
    description = request.json['description']
    price = request.json['price']

    animal = Animal.query.get(animal_uuid)
    center_id = get_jwt_identity()
    if (animal):
        if animal.center_id == Animal.query.filter_by(center_id=center_id).first():
            if animal_name != "None":
                animal.name = animal_name
            if description != "None":
                animal.short_desc = description
            if price != "None":
                animal.price = price
            db.session.commit()
            result = animal_schema.dump(animal)

            data = {
                'message': 'Animal Updated!',
                'status': 200,
                'data': result
            }
            return make_response(jsonify(data)), logging.debug("Animal updated!")
        else:
            return logging.error("It isnt your animal")

    else:
        return logging.error("Animal doesn't exist")


@app.route("/animal_delete/<path:animal>", methods=["DELETE"])
@jwt_required()
def delete_animal():
    animal_uuid = request.json['animal_uuid']
    animal = Animal.query.get(animal_uuid)
    center_id = get_jwt_identity()
    if (animal):
        if animal.center_id == Animal.query.filter_by(center_id=center_id).first():
            db.session.delete(animal)
            db.session.commit()

            data = {
                'message': 'Animal Deleted!',
                'status': 200
            }
            return make_response((jsonify(data))), logging.debug("Animal deleted")
        else:
            return logging.error("It isn't your animal!")
    else:
        return logging.error("Invalid animal id")