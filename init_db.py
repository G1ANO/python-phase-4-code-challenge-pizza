#!/usr/bin/env python3
import sys
import os

# Add server directory to path
sys.path.append('server')

from flask import Flask
from models import db, Restaurant, Pizza, RestaurantPizza

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = f"sqlite:///{os.path.join(BASE_DIR, 'server', 'app.db')}"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

def init_database():
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if data already exists
        if Restaurant.query.count() > 0:
            print("Database already has data. Skipping seed.")
            return
        
        # Add restaurants
        r1 = Restaurant(name="Karen's Pizza Shack", address="address1")
        r2 = Restaurant(name="Sanjay's Pizza", address="address2")
        r3 = Restaurant(name="Kiki's Pizza", address="address3")
        
        # Add pizzas
        p1 = Pizza(name="Emma", ingredients="Dough, Tomato Sauce, Cheese")
        p2 = Pizza(name="Geri", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")
        p3 = Pizza(name="Melanie", ingredients="Dough, Sauce, Ricotta, Red peppers, Mustard")
        
        db.session.add_all([r1, r2, r3, p1, p2, p3])
        db.session.commit()
        
        # Add some restaurant pizzas
        rp1 = RestaurantPizza(price=1, restaurant_id=r1.id, pizza_id=p1.id)
        db.session.add(rp1)
        db.session.commit()
        
        print("Database initialized with seed data!")
        print(f"Restaurants: {Restaurant.query.count()}")
        print(f"Pizzas: {Pizza.query.count()}")
        print(f"RestaurantPizzas: {RestaurantPizza.query.count()}")

if __name__ == "__main__":
    init_database()
