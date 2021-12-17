"""MAINLY NIKITAS CODE, JUST MADE AFEW CHANGES SO IT ALL RUNS TOGETHER!!!"""

from flask import Flask, jsonify, request
from user_db_utils import add_user, _get_user, delete_user, verify_login, update_user_name, update_user_email
from wishlist_db_utils import delete_wishlist

app = Flask(__name__)

# getting the profile for one user
@app.route('/profile/<int:user_id>', methods=['GET'])
def get_users(user_id):
    user = _get_user(user_id)
    return jsonify(user)

## route that changes username 
## added old user name so that they can verify its the write person
@app.route('/profile/change/<int:user_id>/<old_user_name>/<new_user_name>')
def change_user_name(user_id,old_user_name, new_user_name):
    result = update_user(user_id,old_user_name,new_user_name)
    return jsonify(result)

@app.route('/profile/change/email/<int:user_id>/<old_user_email>/<new_user_email>')
def change_user_email(user_id, old_user_email, new_user_email):
    result = update_user_email(user_id, old_user_email, new_user_email)
    return jsonify(result)

## api endpoint that adds new user by inputing dictionary in form of
# user_dict = { 'User_Name':'sophie123','Name_User','Sophie', 'Email_Address':'sophie@gmail.com'}
## user_id is added in the database code so no need to input it

@app.route('/register', methods=['POST'])
def user_acc():
    user = request.get_json()
    add_user(
        User_Name=user['User_Name'],
        Name_User=user['Name_User'],
        Email_Address=user['Email_Address'],
    )
    return user

# deleting a user using the user id
@app.route('/delete/<int:user_id>')

def delete_user_(user_id):
    wish = delete_wishlist(user_id)  ## deletes everything in wishlist too otherwise foregin key restraint
    user = delete_user(user_id)
    return jsonify(user)

## login endpoint that double checks if user exists
## takes similar dictionary to above and returns boolean or string(if there are multiple entries)

@app.route("/login/<string:username>/<string:email>", methods=["GET"])
def verify_login_api(username,email):
    login_dict = request.get_json()

    answer = verify_login( #answer is either {"verify": False}, {"verify": True, "user_id": user_id} or Duplicate users
        username = username,
        email_address = email
    )

    return jsonify(answer)

if __name__ == '__main__':
    app.run(port=5004,debug=True)
