"""MAINLY NIKITAS CODE, JUST MADE AFEW CHANGES SO IT ALL RUNS TOGETHER!!!"""
from flask import Flask, jsonify, request
from user_db_utils import add_user, _get_user, delete_user, verify_login, update_user
from wishlist_db_utilsver import delete_wishlist

app = Flask(__name__)

# getting the profile for one user
@app.route('/profile/<int:user_id>', methods=['GET'])
def get_users(user_id):
    user = _get_user(user_id)
    return jsonify(user)

# adding a user
## added old user name so that they can verify its the write person
@app.route('/profile/change/<int:user_id>/<old_user_name>/<new_user_name>')
def change_user_name(user_id,old_user_name, new_user_name):
    result = update_user(user_id,old_user_name,new_user_name)
    return jsonify(result)



@app.route('/register', methods=['POST'])
def user_acc():
    user = request.get_json()
    add_user(
        User_Name=user['User_Name'],
        Name_User=user['Name_User'],
        Email_Address=user['Email_Address'],
    )
    return user

# deleting a user
@app.route('/delete/<int:user_id>')

def delete_user_(user_id):
    wish = delete_wishlist(user_id)
    user = delete_user(user_id)
    return jsonify(user)


@app.route("/login", methods=["POST"])
def verify_login_api():
    login_dict = request.get_json()
    answer = verify_login(
        user_id = login_dict['User_ID'],
        username = login_dict['User_Name'],
        name_user = login_dict['Name_User'], 
        email_address = login_dict['Email_Address']
    )

    return jsonify(answer)

if __name__ == '__main__':
    app.run(port=5004,debug=True)
