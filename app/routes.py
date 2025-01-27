from flask import Blueprint, jsonify, request
from app.models.planet import Planet
from app import db

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

@planets_bp.route("", methods = ["GET", "POST"])
def get_planets():
    if request.method == "GET":
        planets = Planet.query.all()
        planets_response = []
        for planet in planets:
            planets_response.append({
                "id": planet.id,
                "name": planet.name,
                "description": planet.description,
                "sign": planet.sign
            })
        if not planets_response:
            return jsonify("There are no planets yet! :O", 200)
        return jsonify(planets_response)
    elif request.method == "POST":
        request_body = request.get_json()
        if "name" not in request_body or "description" not in request_body or "sign" not in request_body:
            return jsonify("Invalid request", 400)
        
        new_planet = Planet(
            name = request_body["name"],
            description = request_body["description"],
            sign = request_body["sign"]
        )
        
        db.session.add(new_planet)
        db.session.commit()

        return f"Planet {new_planet.name} created.", 201


@planets_bp.route("/<planet_id>", methods = ["GET", "PUT", "DELETE"])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify(f"Planet with ID {planet_id} not found."), 404

    if request.method == "GET":
        return {
            "name": planet.name,
            "description": planet.description,
            "sign": planet.sign
        }
    
    elif request.method == "PUT":
        request_body = request.get_json()
        planet.name = request_body["name"]
        planet.description = request_body["description"]
        planet.sign = request_body["sign"]

        db.session.commit()

        return jsonify(f"Planet nummber {planet.id} successfully updated!")

    elif request.method == "DELETE":
        db.session.delete(planet)
        db.session.commit()

        return jsonify(f"Planet {planet.name} successfully deleted! bye bitch")

    # for planet in planets:
    #     if planet.name.lower() == planet_name.lower():
    #         planet_response = {
    #             "id": planet.id,
    #             "name": planet.name,
    #             "description": planet.description,
    #             "sign": planet.sign
    #         }
    # return planet_response
