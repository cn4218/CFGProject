import requests
import json
from user_db_utils import get_user_id


class MockFrontEnd:
        
    def get_profile_by_id(self,user_id):
        result = requests.get(
            "http://127.0.0.1:5004/profile/{}".format(user_id),
            headers = {"content_type": "application/json"},

        )
        #results = _map_values(result)
        return result.json()

    def add_new_user(self,user_name,name,email):

        user = {
            "User_Name": user_name,
            "Name_User": name,
            "Email_Address":email

        }
        result = requests.post(
            "http://127.0.0.1:5004/register",
            headers={"content_type":"application/json"},
            data = json.dumps(user),
        )
        return result.json()

    def delete_user_func(self,user_id):
        result = requests.get(
            "http://127.0.0.1:5004/delete/{}".format(user_id),
            headers= {"content_type": "application/json"}
        )
        print(result)
        return result.json()


    def user_login(self,user_id,user_name,name,email):
        user = {
            "User_ID": user_id,
            "User_Name": user_name,
            "Name_User": name,
            "Email_Address":email

        }
        result = requests.post(
            "http://127.0.0.1:5004/login",
            headers = {"content_type":"application/json"},
            data = json.dumps(user),
        )
        return result.json()


    def welcome_message(self):
        print("############################")
        print("Hello, welcome to Cosmo")
        print("############################")
        print()
        i = 0
        while i<=2:
    
        ### put exception handling here!!!
            try:
                answer = input('Would you like to make an account, y/n? ')
                if answer != 'y' and answer !='n':
                    raise Exception
            except:
                print('Your answer has NOT been given in the requested format')
                i+=1

            finally:
                if answer == 'y' or answer== 'n':
                    return answer

        answer = 'Too many tries inputting the incorrect format'
        print(answer)
        return answer


    def enter_details(self):
        self.username = input('Enter your username: ')
        self.nameuser = input('Enter your name: ')
        self.emailaddress = input('Enter your email address: ')
        result = self.add_new_user(self.username,self.nameuser,self.emailaddress)
        return result

    def verify_account_added(self):
        self.user_id = get_user_id(self.username,self.nameuser,self.emailaddress)
        verify_account = self.user_login(self.user_id, self.username,self.nameuser,self.emailaddress)
        return verify_account

    def displaying_user(self):
        print('Account has been created successfully')
        display_user_details = self.get_profile_by_id(self.user_id)  
        print(display_user_details)
        return display_user_details

    def deleting_account(self):
        ans = input('Would you like to delete your account, y/n? ')
        try: 
            if ans!= 'y' and ans!='n':
                raise Exception
            elif ans == 'y':
                dict = self.delete_user_func(self.user_id)
                if dict == {}:
                    print('Account successfully deleted') 
            return dict
        except:
            print('Your answer has NOT been given in the requested format')



def run():
    mock = MockFrontEnd()
    answer = mock.welcome_message()

    if answer == 'y':
        result = mock.enter_details()
        verify_account = mock.verify_account_added()
        if verify_account:
            mock.displaying_user()
            mock.deleting_account()
        else:
            print('Issue creating user')


if __name__ =='__main__':
    run()

