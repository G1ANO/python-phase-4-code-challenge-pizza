#!/usr/bin/env python3
from flask_migrate import Migrate
from flask import Flask, request
from flask_restful import Api, Resource
from models import db, Restaurant, Pizza, RestaurantPizza
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


class RestaurantsResource(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        return [r.to_dict(only=('id', 'name', 'address')) for r in restaurants], 200


class RestaurantByIdResource(Resource):
    def get(self, id):
        restaurant = Restaurant.query.get(id)
        if not restaurant:
            return {"error": "Restaurant not found"}, 404
        return restaurant.to_dict(only=('id', 'name', 'address', 'restaurant_pizzas')), 200

    def delete(self, id):
        restaurant = Restaurant.query.get(id)
        if not restaurant:
            return {"error": "Restaurant not found"}, 404
        db.session.delete(restaurant)
        db.session.commit()
        return '', 204


class PizzasResource(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        return [p.to_dict(only=('id', 'name', 'ingredients')) for p in pizzas], 200


class RestaurantPizzasResource(Resource):
    def post(self):
        data = request.get_json()
        try:
            price = data.get("price")
            pizza_id = data.get("pizza_id")
            restaurant_id = data.get("restaurant_id")
            pizza = Pizza.query.get(pizza_id)
            restaurant = Restaurant.query.get(restaurant_id)
            if not pizza or not restaurant:
                raise ValueError("Invalid pizza or restaurant")
            restaurant_pizza = RestaurantPizza(
                price=price,
                pizza_id=pizza_id,
                restaurant_id=restaurant_id
            )
            db.session.add(restaurant_pizza)
            db.session.commit()
            return restaurant_pizza.to_dict(only=(
                'id', 'price', 'pizza_id', 'restaurant_id', 'pizza', 'restaurant'
            )), 201
        except Exception:
            return {"errors": ["validation errors"]}, 400


api.add_resource(RestaurantsResource, "/restaurants")
api.add_resource(RestaurantByIdResource, "/restaurants/<int:id>")
api.add_resource(PizzasResource, "/pizzas")
api.add_resource(RestaurantPizzasResource, "/restaurant_pizzas")

if __name__ == "__main__":
    app.run(port=5555, debug=True)
