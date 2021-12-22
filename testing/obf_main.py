import requests
import json

class MockProductFrontEnd:

    def get_every_product(self,order,ingredient1,boolean1,ingredient2,boolean2,ingredient3,boolean3,ingredient4,boolean4,ingredient5,boolean5):
        product_dict = {
            "filter": order,
            "data": {
            "1" : (ingredient1, boolean1),
            "2": (ingredient2, boolean2),
            "3": (ingredient3, boolean3),
            "4": (ingredient4, boolean4),
            "5": (ingredient5, boolean5)

        }
        }
        result = requests.post(
            "http://127.0.0.1:5001/Search",
            headers = {"content_type": "application/json"},
            data = json.dumps(product_dict)
        )
        print(result)
        return result.json()

    def fetch_existing_search_result(self):
        result = requests.get(
            "http://127.0.0.1:5001/Results",
            headers = {"content_type": "application/json"},
        )
        return result.json()

    

    def welcome_message(self):
        print("############################")
        print("Hello, welcome to Cosmo")
        print("############################")
        print()
    def return_bool(self,answer):
        if answer == 'y':
            return True
        elif answer == 'n':
            return False
        else:
            return ''

    def selecting_ingredients(self):
        ordering_answer = input('Would you like your search to be ordered, y/n? ')

        self.ingredientone = input('What is the first ingredient you would like to search for? ')
        answerone = input('Would you like the products to contain this ingredient, y/n? ' )
        self.booleanone = self.return_bool(answerone)
        self.ingredienttwo = input('What is the second ingredient you would like to search for? ')
        answertwo = input('Would you like the products to contain this ingredient, y/n? ')
        self.booleantwo = self.return_bool(answertwo)
        self.ingredientthree = input('What is the third ingredient you would like to search for? ')
        answerthree = input('Would you like the products to contain this ingredient, y/n? ')
        self.booleanthree = self.return_bool(answerthree)
        self.ingredientfour = input('What is the fourth ingredient you would like to search for? ')
        answerfour = input('Would you like the products to contain this ingredient, y/n? ')
        self.booleanfour = self.return_bool(answerfour)
        self.ingredientfive = input('What is the fifth ingredient you would like to search for? ')
        answerfive = input('Would you like the product to contain this ingredient, y/n? ')
        self.booleanfive = self.return_bool(answerfive)
        if ordering_answer == 'y':
            ordering = 'ordered'
        elif ordering_answer == 'n':
            ordering = 'unordered'
        else:
            print('Error with input in last question')
        self.ordering = ordering

    def input_products(self):

        list_products = self.get_every_product(order = self.ordering,ingredient1= self.ingredientone,boolean1 = self.booleanone,
        ingredient2 = self.ingredienttwo,boolean2 = self.booleantwo,ingredient3 = self.ingredientthree,boolean3 = self.booleanthree,
        ingredient4 = self.ingredientfour,boolean4 = self.booleanfour,ingredient5= self.ingredientfive,boolean5 = self.booleanfive)
        return list_products

    def results_again(self):
        answer = input('Would you like to see your search results again, y/n? ')
        if answer == 'y':
            result = self.fetch_existing_search_result()
        else:
            result = 'Goodbye!'
            print('Goodbye!')
        return result


def run():
    mock = MockProductFrontEnd()
    # result = mock.get_every_product('unordered','water',True,'water',False,'','','','','','')
    # res2 = mock.fetch_existing_search_result()
    # print(result)
    # print(res2)
    #'y','water','y','Stearalkonium chloride','y','stearyl alcohol','y','butyrospermum parkii (beurre de karité)','n','caprylic/capric triglyceride','n'

    mock.welcome_message()
    mock.selecting_ingredients()
    list_products_ = mock.input_products()
    result_dict={}
    if not isinstance(list_products_,str):
        result_dict = mock.results_again()
    # print(list_products_)
    # print('Results: ',result_dict)
    return list_products_,result_dict

if __name__ == '__main__':

    output = run()
