"""
Initialization Module
"""
from flask import Flask, g
from pymongo import MongoClient
from werkzeug.local import LocalProxy

app = Flask(__name__)
app.config.from_object("app.config.DevelopmentConfig")

mongo = MongoClient(app.config["MONGO_URI"])
db = mongo.splitwise

from app.routes import register_routes

register_routes(app)
