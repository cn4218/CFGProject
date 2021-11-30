import time
from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
# import ast

products_path = './products.csv'  #  This should be the OBF CSV


app = Flask(__name__, static_folder='../build', static_url_path='/')
api = Api(app)

"""
These 3 functions 
"""
@app.errorhandler(404)
def not_found(e):
	return app.send_static_file('index.html')


@app.route('/')
def index():
	return app.send_static_file('index.html')


@app.route('/api/time')
def get_current_time():
	return {'time': time.time()}


# # COMPANIES endpoint (/companies)
# # GET and POST methods to retrieve and add company data
# class Companies(Resource):
#
# 	def get(self):
# 		data = pd.read_csv(companies_path)   # read local csv
# 		data = data.todict()    # converts dataframe to dictionary
# 		return {'data': data}, 200    # returns data and 200 OK
#
# 	def post(self):
# 		parser = reqparse.RequestParser()    # Initialise
# 		parser.add_argument('company_id', required = True, type = int)
# 		parser.add_argument('company_name', required = True, type = str)
# 		parser.add_argument('city', required = True, type = str)
# 		parser.add_argument('industry', required = True, type = str)
# 		parser.add_argument('nb_employees', required = True, type = int)
# 		parser.add_argument('size_office', required = True, type = int)
# 		args = parser.pass_args()
# 		return {
# 			       'id': args['company_id'],
# 			       'name': args['company_name'],
# 			       'city': args['city'],
# 			       'industry': args['industry'],
# 			       'nb_employees': args['nb_employees'],
# 			       'size_office': args['size_office'],
# 		       }, 201
#
# api.add_resource(Companies, '/companies')

app.run()

if __name__ == '__main__':
	app.run(debug=True)