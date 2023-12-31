# from pymongo import MongoClient
# client = MongoClient("mongodb://127.0.0.1:27017")
# db=client.test_database
# my_collection = db["my_collection"]

# # Insert a document into the collection
# document = {"name": "John", "age": 30, "city": "New York"}
# my_collection.insert_one(document)

# # Query the collection
# results = my_collection.find_one({"city": "New York"})
# print(results._id)
# from flask import Flask, request

# # Flask constructor takes the name of
# # current module (__name__) as argument.
# app = Flask(__name__)

# # The route() function of the Flask class is a decorator,
# # which tells the application which URL should call
# # the associated function.
# @app.route('/<id>')
# # ‘/’ URL is bound with hello_world() function.
# def hello_world(id):
#     print(request.args)
#     return 'Hello World'

# # main driver function
# if __name__ == '__main__':

#     # run() method of Flask class runs the application
#     # on the local development server.
#     app.run()

from enum import StrEnum


class name(StrEnum):
    one = "two"


print([xx.value for xx in name])
