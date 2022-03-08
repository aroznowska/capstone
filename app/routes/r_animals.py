from app import app, db

from app.models.animals import Animal
from app.models.centers import Center
from app.models.species import Specie
from sqlalchemy import select
from app.schemas import center_schema, centers_schema, animal_schema, animals_schema, specie_schema, species_schema

import argparse
import logging

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from sqlalchemy import text
from flask_restful import reqparse, abort, Api, Resource
from flask import request, jsonify, make_response


jwt = JWTManager(app)
@app.route("/register", methods=["POST"])
def register_center(center_id):
    parser = argparse.ArgumentParser()  # only allow price changes, no name changes allowed
    parser.add_argument('center_name', type=str, required=True,
                        help="string type, this field cannot be left blank")
    parser.add_argument('password', type=str, required=True,
                        help="Must enter the center password (type = str)"
                        )
    parser.add_argument('adress', type=str, required=False, default="None",
                        help="This field can be left blank (type = str)")
    args = parser.parse_args()
    new_center = Center(center_id, args.center_name, args.password, args.adress)

    db.session.add(new_center)
    db.session.commit()

    result = center_schema.dump(new_center)

    data = {
            'message': 'New Center Created!',
            'status': 201,
            'data': result
        }
    return logging.debug('New Center: ', data)

@app.route("/login", methods=["GET", "POST"])
def login_center(center_id, center_name, password):
    parser = argparse.ArgumentParser()  # only allow price changes, no name changes allowed
    parser.add_argument('center_name', type=str, required=True,
                        help="string type, this field cannot be left blank")
    parser.add_argument('password', type=str, required=True,
                        help="Must enter the center password (type = str)"
                        )

    args = parser.parse_args()
    center = Center.query.filter_by(center_name=args.center_name).one_or_none()
    if not center or not center.check_password(password):
        return logging.error('Wrong center name or password')
    center_id = center.center_id
    access_token = create_access_token(identity=center_id)
    json_access_token = jsonify(access_token=access_token)
    return json_access_token, access_token, logging.debug('logged succesfully')

@app.route("/centers", methods=["GET"])
def get_centers():
    all_center = Center.query.all()
    result = centers_schema.dump(all_center)

    data = {
        'message': 'All Centers!',
        'status': 200,
        'data': result
    }
    return make_response(jsonify(data))


# endpoint to GET author detail by id
@app.route("/center/<int:center_id>", methods=["GET"])
def get_center(center_id):
    center = Center.query.get(center_id)
    animals = [animal.animal_info_json for animal in Animal.query.filter_by(center_id=center_id).all()]
    if (center):
        result = center_schema.dump(center)
        data = {
            'message': 'Center Info!',
            'status': 200,
            'data': result,
            'animals': animals
        }
        logging.debug(data)
    else:
        data = {
            'message': 'Invalid Center ID!',
            'status': 200
        }
        logging.error('Invalid center_id')
    return make_response(jsonify(data))


"""
===========================
endpoints for Book CRUD
===========================
"""

@app.route("/animal", methods=["POST"])
@jwt_required
def add_animal(animal_uuid):
    parser = argparse.ArgumentParser()  # only allow price changes, no name changes allowed
    parser.add_argument('name', type=str, required=True,
                        help="string type, this field cannot be left blank")
    parser.add_argument('age', type=str, required=True,
                        help="Must enter the center password (type = str), format: DD-MM-YYYY"
                        )
    parser.add_argument('short_desc', type=str, required=False, default="None",
                        help="This field can be left blank (type = str)")
    parser.add_argument('price', type=float, required=False, default=0.00,
                        help="This field can be left blank (type = float), default = 0.00")
    parser.add_argument('specie_name', type=str, required=True,
                        help="Must enter the center password (type = str)"
                        )
    args = parser.parse_args()

    if Specie.query.filter_by(specie_name=args.specie_name).one_or_none():
        center_id = get_jwt_identity()
        new_animal = Animal(animal_uuid, args.name.lower(), args.age, args.short_desc, args.price, args.specie_name,
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


@app.route("/animal/<path:animal_uuid>", methods=["PUT"])
@jwt_required
def update_animal(animal_uuid):

    parser = argparse.ArgumentParser()  # only allow price changes, no name changes allowed
    parser.add_argument('name', type=str, required=False, default="None",
                        help="string type, this field cannot be left blank, (type = str), default = None")
    parser.add_argument('short_desc', type=str, required=False, default="None",
                        help="This field can be left blank (type = str), default = None")
    parser.add_argument('price', type=float, required=False, default=0.00,
                        help="This field can be left blank (type = float), default = 0.00")
    args = parser.parse_args()

    animal = Animal.query.get(animal_uuid)
    center_id = get_jwt_identity()
    if (animal):
        if animal.center_id == Animal.query.filter_by(center_id=center_id).first():
            if args.name != "None":
                animal.name = args.name.lower()
            if args.short_desc != "None":
                animal.short_desc = args.short_desc
            if args.price != 0.00:
                animal.price = args.price
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


@app.route("/animal/<path:animal>", methods=["DELETE"])
@jwt_required
def delete_animal(animal_uuid):
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