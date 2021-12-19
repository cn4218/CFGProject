

import json
from flask import Flask, jsonify, request
from user_db_utils import dbConnection
from wishlist_db_utils import delete_wishlist

app = Flask(__name__)

db_utils = dbConnection('blu3bottl3')

# getting the profile for one user
@app.route('/profile/<int:user_id>', methods=['GET'])
def get_users(user_id):
    user = db_utils._get_user(user_id)
    return jsonify(user)

## route that changes username 
## added old user name so that they can verify its the write person
@app.route('/profile/change/<int:user_id>/<old_user_name>/<new_user_name>')
def change_user_name(user_id,old_user_name, new_user_name):
    result = db_utils.update_user_name(user_id,old_user_name,new_user_name)
    return jsonify(result)   ##return boolean TRUE or FALSE if user details have been updated

@app.route('/profile/change/email/<int:user_id>/<old_user_email>/<new_user_email>')
def change_user_email(user_id, old_user_email, new_user_email):
    result = db_utils.update_user_email(user_id, old_user_email, new_user_email)
    return jsonify(result)


## api endpoint that adds new user by inputing dictionary in form of
# user_dict = { 'User_Name':'sophie123','Name_User','Sophie', 'Email_Address':'sophie@gmail.com'}
## user_id is added in the database code so no need to input it
@app.route('/register', methods=['POST'])
def user_acc():
    user = request.get_json()

    answer = db_utils.add_user(
        user_name=user['User_Name'],
        name_user=user['Name_User'],
        email_address=user['Email_Address']
    )
    if answer == True:
        return user
    else:
        return jsonify(answer)



# deleting a user using the user id
@app.route('/delete/<int:user_id>')

def delete_user_(user_id):
    wish = delete_wishlist(user_id)  ## deletes everything in wishlist too otherwise foregin key restraint
    user = db_utils.delete_user(user_id)
    print(user)
    return jsonify(user)


## login endpoint that double checks if user exists
## takes similar dictionary to above and returns boolean or string(if there are multiple entries)

@app.route("/login/<string:username>/<string:email>", methods=["GET"])
def verify_login_api(username,email):

    #answer is either {"verify": False}, {"verify": True, "user_id": user_id} or Duplicate users
    answer = db_utils.verify_login(username,email)

    return jsonify(answer)

if __name__ == '__main__':
    app.run(port=5004,debug=True)
