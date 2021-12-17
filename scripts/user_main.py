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


    def user_login(self,user_name,email):

        result = requests.get(
            "http://127.0.0.1:5004/login/{}/{}".format(user_name,email),
            headers = {"content_type":"application/json"},
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
                print(answer)
                if answer != 'y' and answer !='n':
                    raise Exception
            except:
                print('Your answer has NOT been given in the requested format')
                i+=1

            finally:
                if answer == 'y' or answer=='n':
                    return answer

        answer = 'Too many tries inputting the incorrect format'
        return answer


    def enter_details(self):

        self.username = input('Enter your username: ')
        self.nameuser = input('Enter your name: ')
        self.emailaddress = input('Enter your email address: ')

        result = self.add_new_user(self.username,self.nameuser,self.emailaddress)

        return result

    def verify_account_added(self):
        self.user_id = get_user_id(self.username,self.nameuser,self.emailaddress)
        verify_account = self.user_login(self.username,self.emailaddress)
        return verify_account

    def displaying_user(self):
        print('Account has been created successfully')
        display_user_details = self.get_profile_by_id(self.user_id)  
        return display_user_details

    def deleting_account(self):
        ans = input('Would you like to delete your account, y/n? ')
        try: 
            if ans != 'y' and ans !='n':
                issue = 'Your answer has NOT been given in the requested format'
                raise Exception(issue)
            elif ans == 'y':
                result = self.delete_user_func(self.user_id)
                if result == "Account successfully deleted for user {}".format(self.user_id):
                    print('Account successfully deleted') 
                    return 'Account successfully deleted'

            elif ans == 'n':
                return ans
            return result
        except:
            print(issue)
            return issue
    


def run():
    mock = MockFrontEnd()
    issue = None
    ans = 'Issue with run function'

    answer = mock.welcome_message()
    if answer == 'y':
        try:
            result = mock.enter_details()
            print(result)
            if result == 'User details already exist, try again with a new username':
                issue = result
                raise Exception(issue)
            elif result == "Error creating account: Your email address has NOT been given in the requested format":
                issue = result
                raise Exception(issue)
            else:
                verify_account = mock.verify_account_added()
                print(verify_account)
                if verify_account['verify'] == False:
                    issue = 'Account has not been added to database'
                    raise Exception(issue)
                else:
                    user_details = mock.displaying_user()
                    print(result)
                    ans = mock.deleting_account()

        except:
            print('Issue creating user')
            if issue is not None:
                run_result =  'Issue: ' + issue
            else:
                run_result = 'Issue creating user'
            ans = run_result
 
        finally:
            if ans == 'n':
                run_result =  result
            else:
                run_result = ans
        return run_result
    else:
        return 'Goodbye!'


if __name__ =='__main__':
    output = run()
