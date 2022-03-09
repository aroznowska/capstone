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
@app.route("/")
def hello():
    return "hello"


@app.route("/register", methods=["POST"])
def register_center():

    center_name = request.json['center_name']
    password = request.json['password']
    adress = request.json['adress']

    new_center = Center(center_name, password, adress)

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
def login_center(center_name, password):

    center_name = request.json['center_name']
    password = request.json['password']

    center = Center.query.filter_by(center_name=center_name).one_or_none()
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


@app.route("/center/<int:center_id>", methods=["GET"])
def get_center(center_id):
    center = Center.query.get(center_id)
    animals = [animal.animal_info_json_simpl for animal in Animal.query.filter_by(center_id=center_id).all()]
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

