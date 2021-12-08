from flask import Flask, jsonify, request
from db_utils import add_user, _get_user, delete_user

app = Flask(__name__)


# adding a user

@app.route('/register', methods=['PUT'])
def user_acc():
    user = request.get_json()
    add_user(
        User_ID=user['User_ID'],
        Name_User=user['Name_User'],
        Email_Address=user['Email_Address'],
    )
    return user


# getting the profile for one user
@app.route('/profile/<int:user_id>/<username>', methods=['GET'])
def get_users(User_ID, User_Name):
    user = _get_user(User_ID, User_Name)
    return jsonify(user)

# deleting a user
@app.route('/delete/<int:user_id>')
def delete_user(User_ID):
    user = delete_user(User_ID)
    return jsonify(user)

if __name__ == '__main__':
    app.run(debug = True)