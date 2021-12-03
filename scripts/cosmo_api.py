# This is an attempt to reuse here some modules and functions I discovered
# for another project, but in the end because I wasn't sure how to use them, I stuck
# to the usual Flask.

import time
from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
# import ast

products_path = './products.csv'  #  This should be the OBF CSV


app = Flask(__name__, static_folder='../build', static_url_path='/')
api = Api(app)


@app.errorhandler(404)
def not_found(e):
	return app.send_static_file('index.html')


@app.route('/')
def index():
	return app.send_static_file('index.html')


@app.route('/api/time')
def get_current_time():
	return {'time': time.time()}


# # PRODUCTS endpoint (/products)
# # GET and POST methods to retrieve and add product data
# class Products(Resource):
#
# 	def get(self):
# 		data = pd.read_csv(products_path)   # read local csv
# 		data = data.todict()    # converts dataframe to dictionary
# 		return {'data': data}, 200    # returns data and 200 OK
#
# 	def post(self):
# 		parser = reqparse.RequestParser()    # Initialise
# 		parser.add_argument('productID', required = True, type = int)
# 		parser.add_argument('code', required = True, type = int)
# 		parser.add_argument('product_name', required = True, type = str)
# 		parser.add_argument('ingredients_list', required = True, type = str)

# 		args = parser.pass_args()
# 		return {
# 			       'id': args['product_id'],
# 			       'name': args['product_name'],
# 			       'city': args['city'],
# 			       'industry': args['industry'],
# 			       'nb_employees': args['nb_employees'],
# 			       'size_office': args['size_office'],
# 		       }, 201
#
# api.add_resource(Products, '/products')

# app.run()

if __name__ == '__main__':
	app.run(debug=True)