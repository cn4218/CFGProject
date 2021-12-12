import requests
import json

  
def get_profile_by_id(user_id):
    result = requests.get(
        "http://127.0.0.1:5003/profile/{}".format(user_id),
        headers = {"content_type": "application/json"},

    )
    #results = _map_values(result)
    return result.json()

answer = get_profile_by_id(1)
print('h',answer)
def add_new_user(user_id,user_name,name,email):
    user = {
        "User_ID": user_id,
        "User_Name": user_name,
        "Name_User": name,
        "Email_Address":email

    }
    result = requests.post(
        "http://127.0.0.1:5003/register",
        headers={"content_type":"application/json"},
        data = json.dumps(user),
    )
    return result.json()



def delete_user_func(user_id):
    result = requests.get(
        "http://127.0.0.1:5003/delete/{}".format(user_id),
        headers= {"content_type": "application/json"}
    )
    print(result)
    return result.json()


ans = delete_user_func(4)
print('ans',ans)

def user_login(user_id,user_name,name,email):
    user = {
        "User_ID": user_id,
        "User_Name": user_name,
        "Name_User": name,
        "Email_Address":email

    }
    result = requests.post(
        "http://127.0.0.1:5003/login",
        headers = {"content_type":"application/json"},
        data = json.dumps(user),
    )
    return result.json()



