#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

# Route for getting all restaurants
@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([restaurant.as_dict() for restaurant in restaurants]), 200

# Route for getting a specific restaurant by ID
@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get_or_404(id)
    return jsonify(restaurant.as_dict()), 200

# Route for deleting a specific restaurant by ID
@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get_or_404(id)
    db.session.delete(restaurant)
    db.session.commit()
    return make_response('', 204)

# Route for getting all pizzas
@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([pizza.as_dict() for pizza in pizzas]), 200

# Route for creating a restaurant_pizza
@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()
    pizza_id = data.get('pizza_id')
    restaurant_id = data.get('restaurant_id')
    price = data.get('price')

    if not (1 <= price <= 30):
        return jsonify({"error": "Price must be between 1 and 30"}), 400

    restaurant_pizza = RestaurantPizza(pizza_id=pizza_id, restaurant_id=restaurant_id, price=price)
    db.session.add(restaurant_pizza)
    db.session.commit()
    return jsonify(restaurant_pizza.as_dict()), 201


if __name__ == "__main__":
    app.run(port=5555, debug=True)












# from models import db, Restaurant, RestaurantPizza, Pizza
# from flask_migrate import Migrate
# from flask import Flask, request, jsonify, make_response
# # Import Resource from Flask-RESTful
# from flask_restful import Api, Resource

# import os

# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.json.compact = False

# migrate = Migrate(app, db)

# db.init_app(app)

# # Create an Api instance from Flask-RESTful
# api = Api(app)


# @app.route("/")
# def index():
#     return "<h1>Code challenge</h1>"


# # Route for getting all restaurants (using Resource class)
# class RestaurantList(Resource):
#     def get(self):
#         restaurants = Restaurant.query.all()
#         return jsonify([restaurant.as_dict() for restaurant in restaurants]), 200


# api.add_resource(RestaurantList, '/restaurants')


# # Route for getting a specific restaurant by ID (using Resource class)
# class RestaurantDetails(Resource):
#     def get(self, id):
#         restaurant = Restaurant.query.get_or_404(id)
#         return jsonify(restaurant.as_dict()), 200


# api.add_resource(RestaurantDetails, '/restaurants/<int:id>')


# # Route for deleting a specific restaurant by ID (using make_response)
# @app.route('/restaurants/<int:id>', methods=['DELETE'])
# def delete_restaurant(id):
#     restaurant = Restaurant.query.get_or_404(id)
#     db.session.delete(restaurant)
#     db.session.commit()
#     return make_response('', 204)  # Empty response with status code

# # ... other routes (can be converted to Resource classes as needed)

# if __name__ == "__main__":
#     app.run(port=5555, debug=True)
