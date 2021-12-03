## app.py ---  API UI/Users SQL DB
## NIKITA's job!
from flask import Flask, jsonify, request
from users_data import users
from db_utils_users import search_user, get_userID

app = Flask(__name__)

# GET to retrieve data
# Endpoint to get all the users
@app.route("/users/")
def get_users():
	return jsonify(users)

# GET to retrieve data
# Endpoint to get a user with a specific userID
@app.route("/users/<int:id>")
def get_user_by_id(id):
	user = search_user(userID, users)
	return jsonify(user)

# To get user 555
# http://127.0.0.1:5000/users/555


# POST to add data
@app.route("/users", methods=["POST"])
def add_user():
	user = request.get_json()
	# validate_user(user)  # some sort of data validation to force json keys
	users.append(user)
	return user

# PUT to update data
@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
	user_to_update = request.get_json()
	index = get_index(userID, users)
	users[index] = user_to_update
	return jsonify(users[index])

# DELETE to remove data
@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
	index = get_index(userID, users)
	deleted = users.pop(index)
	return jsonify(deleted)


if __name__ == '__main__':
	app.run(debug=True)


