


# Product class — fields should correspond to those in the SQL DB Products table

class Product:
	def __init__(self, name, ingredients, brand, category):
		self.name = name
		self.ingredients = ingredients
		self.brand = brand
		self.category = category


# User class — fields should correspond to those in the SQL DB Users table

class User:
	def __init__(self, first_name, last_name, email):
		self.first_name = first_name
		self.last_name = last_name
		self.email = email


if __name__ == '__main__':
	# run()
	pass