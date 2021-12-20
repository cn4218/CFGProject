import json
from flask import Flask, jsonify, request
from user_db import add_user, _get_user, delete_user, verify_login, update_user_name, update_user_email
from user_db import dbConnection
from wishlist_db_utils import delete_wishlist

app = Flask(__name__)

db_utils = dbConnection('skittle1')


# getting the profile for one user
@app.route('/profile/<int:user_id>', methods=['GET'])
def get_users(user_id):
    """
        API endpoint that gets a users profile using their user_id. It uses the _get_user function from user db_utils
        to retrieve all the information associated with the user_id of the user you want information for, it returns
        a dict list which looks similar to:
         { "Email_Address": "nik1@mail.com", "Name_User": "nikita", "User_ID": 2, "User_Name": "niki123"}
        Returns
        --------
        user: dict
            user dictionary with the information for the user which matches with the specified user_id
    """
    user = db_utils._get_user(user_id)
    return jsonify(user)


## route that changes username
## added old user name so that they can verify its the write person
@app.route('/profile/change/<int:user_id>/<old_user_name>/<new_user_name>')
def change_user_name(user_id, old_user_name, new_user_name):
    """
        API endpoint that gets a users profile using their user_id, old_user_name and new_username. It uses the update_user_name
        function from user db_utils using the user_id as a reference to that particular user and verifies that their old user_name
        matches before updating to a new one, it returns a boolean.
        Returns
        --------
        True: bool
                if username is successfully updated
    """
    result = db_utils.update_user_name(user_id, old_user_name, new_user_name)
    return jsonify(result)  ##return boolean TRUE or FALSE if user details have been updated


@app.route('/profile/change/email/<int:user_id>/<old_user_email>/<new_user_email>')
def change_user_email(user_id, old_user_email, new_user_email):
    """
          API endpoint that gets a users profile using their user_id, old_email and new_email. It uses the update_user_email
          function from user db_utils using the user_id as a reference to that particular user and verifies that their old email
          matches before updating to a new one. It returns a boolean.
          Returns
          --------
          True: bool
                  if email is successfully updated
      """
    result = db_utils.update_user_email(user_id, old_user_email, new_user_email)
    return jsonify(result)


## api endpoint that adds new user by inputing dictionary in form of
# user_dict = { 'User_Name':'sophie123','Name_User','Sophie', 'Email_Address':'sophie@gmail.com'}
## user_id is added in the database code so no need to input it
@app.route('/register', methods=['POST'])
def user_acc():
    """
        API endpoint that registers a user into the sql table. Takes in a dictionary, user in format:
        user = { 'User_Name':'sophie123','Name_User','Sophie', 'Email_Address':'sophie@gmail.com'}
        Returns
        --------
        Either:
        user: dict
            user dictionary for the new user that's been added
        OR:
        answer: str
            string containing message on why the user hasn't been added

    """
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
    """
        API endpoint which let's you delete a user by specifying the users user_id. It uses the delete_user function in user_db_utils
        in order to delete the user from the SQL database.
        Returns
        --------
            1. "Account successfully deleted for username niki123"
                    It will return this statement if an account is deleted successfully and will update the SQL database by removing the user
            2. "No entry in database corresponding to given user ID: 2"
                    It will return this statement if you attempt to delete a user which doesn't exist in the SQL database/ if they've already
                    been removed.
    """
    # wish = delete_wishlist(user_id)  ## deletes everything in wishlist too otherwise foregin key restraint
    user = db_utils.delete_user(user_id)
    print(user)
    return jsonify(user)


## login endpoint that double checks if user exists
## takes similar dictionary to above and returns boolean or string(if there are multiple entries)

@app.route("/login/<string:username>/<string:email>", methods=["GET"])
def verify_login_api(username, email):
    """
           API endpoint which let's you check whether a user exists for them to login. It uses the verify_login function from user db_utils
           and with the use of the username & email for verification it will return a dict
           Returns
           --------
           Either:
            1. {
                "user_id": 3,
                "verify": true
                }
                    if the user exists and the username & email can be verified in the SQL database it will return the True boolean and dict above.
            2. {
                "verify": false
                }
                    if the user's username/ email is incorrect or the user does not exist in the SQL database it will return False and the dict above.

             """
    # answer is either {"verify": False}, {"verify": True, "user_id": user_id} or Duplicate users
    answer = db_utils.verify_login(username, email)

    return jsonify(answer)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
