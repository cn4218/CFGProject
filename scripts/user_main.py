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


    def user_login(self,user_name,name,email):
        user = {
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
        return answer


    def enter_details(self):
        try:
            self.username = input('Enter your username: ')
            self.nameuser = input('Enter your name: ')
            self.emailaddress = input('Enter your email address: ')
            if '@' not in self.emailaddress or '.' not in self.emailaddress:
                raise Exception
            result = self.add_new_user(self.username,self.nameuser,self.emailaddress)
        except:
            print('Your email address has NOT been given in the requested format')
            return 'Incorrect Email Input'
        return result

    def verify_account_added(self):
        self.user_id = get_user_id(self.username,self.nameuser,self.emailaddress)
        verify_account = self.user_login(self.username,self.nameuser,self.emailaddress)
        return verify_account

    def displaying_user(self):
        print('Account has been created successfully')
        display_user_details = self.get_profile_by_id(self.user_id)  
        return display_user_details

    def deleting_account(self):
        ans = input('Would you like to delete your account, y/n? ')
        try: 
            if ans != 'y' and ans !='n':
                raise Exception
            elif ans == 'y':
                result = self.delete_user_func(self.user_id)
                if result == "Account successfully deleted for user {}".format(self.user_id):
                    print('Account successfully deleted') 
                    return 'Account successfully deleted'

            elif ans == 'n':
                return ans
            return result
        except:
            print('Your answer has NOT been given in the requested format')
    


def run():
    mock = MockFrontEnd()

    answer = mock.welcome_message()
    if answer == 'y':
        try:
            result = mock.enter_details()
            if result == 'Incorrect Email Input':
                issue = 'Incorrect Email Input'
                raise Exception(issue)
            while result != 'Incorrect Email Input':
                verify_account = mock.verify_account_added()
                print(verify_account)
                if verify_account != True:
                    issue = verify_account
                    raise Exception(issue)
                elif verify_account:
                    user_details = mock.displaying_user()
                    print(result)
                    ans = mock.deleting_account()
                    print(ans)
                break

        except:
            print('Issue creating user')
            run_result =  'Issue creating user: ' + issue
            ans = run_result
        finally:
            if ans == 'n':
                run_result =  result
            else:
                run_result = ans
            return run_result



if __name__ =='__main__':
    output = run()
