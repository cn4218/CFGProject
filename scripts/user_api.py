from flask import Flask, jsonify, request
from user_db_utils import verify_login


app = Flask(__name__)
@app.route("/login/<int:user_id>", method=["POST"])
def verify_login():
    login_dict = request.get_json()
    answer = verify_login(
        user_id = login_dict['UserID'],
        username = login_dict['UserName'],
        name_user = login_dict['NameUser'], 
        email_address = login_dict['EmailAddress']
    )

    return jsonify(answer)