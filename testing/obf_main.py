
import requests
import json
"""
File contains:
MockProductFrontEnd : class
run : function
"""


class MockProductFrontEnd:
    """
    Class that Mocks front end for the products search result
    The class contains functions:
    get_every_product(self,order,ingredient1,boolean1,ingredient2,boolean2,ingredient3,boolean3,ingredient4,boolean4,ingredient5,boolean5)
    fetch_existing_search_result(self)
    welcome_message(self)
    return_bool(self,answer)
    selecting_ingredients(self)
    input_products(self)
    results_again(self)
    """

    def get_every_product(self,order,ingredient1,boolean1,ingredient2,boolean2,ingredient3,boolean3,ingredient4,boolean4,ingredient5,boolean5):
        """
        Formats search query into dicionary and sends post request to API endpoint for function find_products in app.py 

        Parameters
        ----------
        order : str
            ordered or unordered search
        ingredient1 : str
            1st ingredient to search 
        boolean1 : bool
            wether to include or exclude ingredient
        ingredient2 : str
            2nd ingredient to search 
        boolean2 : bool
            wether to include or exclude ingredient
        ingredient3 : str
            3rd ingredient to search 
        boolean3 : bool
            wether to include or exclude ingredient
        ingredient4 : str
            4th ingredient to search 
        boolean4 : bool
            wether to include or exclude ingredient
        ingredient5 : str
            5th ingredient to search 
        boolean5 : bool
            wether to include or exclude ingredient

        Returns
        -------
        result : list
            list of product dictionaries for search result
        """
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
        # print(result)
        return result.json()

    def fetch_existing_search_result(self):
        """
        Mocks sending a get request to retrieve the last queried search result to mock send_results function in app.py

        Returns
        -------
        result : list
            list of product dictionaries for the last queried search results
            empty list of retrives no results

        """
        result = requests.get(
            "http://127.0.0.1:5001/Results",
            headers = {"content_type": "application/json"},
        )
        return result.json()

    

    def welcome_message(self):
        """
        Function that prints welcome message for mock user
        """
        print("############################")
        print("Hello, welcome to Cosmo")
        print("############################")
        print()

    def return_bool(self,answer):
        """
        Formats input answer into a bool to be placed into get_every_product function

        Parameters
        ----------
        answer : str
            answer to input questions

        Returns
        -------
        bool or str

        """
        if answer == 'y':
            return True
        elif answer == 'n':
            return False
        else:
            return ''

    def selecting_ingredients(self):
        """
        Function that uses input function to ask mock user questions about what ingredients they want to search for and if its an ordered search.
        Formats the answers correctly using return_bool.
        Mocks front end search query.
        """
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
        """
        Inputs results from selecting_ingredients function into get_every_product 

        Returns
        -------
        list_products : list
            list of product dictionaries
        """
        list_products = self.get_every_product(order = self.ordering,ingredient1= self.ingredientone,boolean1 = self.booleanone,
        ingredient2 = self.ingredienttwo,boolean2 = self.booleantwo,ingredient3 = self.ingredientthree,boolean3 = self.booleanthree,
        ingredient4 = self.ingredientfour,boolean4 = self.booleanfour,ingredient5= self.ingredientfive,boolean5 = self.booleanfive)
        return list_products

    def results_again(self):
        """
        Mocks front end of retrieving last search result, using input function and running fetch_existing_search_result

        Returns
        -------
        result : list or str
            Either: list of product dictionaries of most recent search
            Or: 'Goodbye!'
        """
        answer = input('Would you like to see your search results again, y/n? ')
        if answer == 'y':
            result = self.fetch_existing_search_result()
        else:
            result = 'Goodbye!'
            print('Goodbye!')
        return result


def run():
    """
    Function that runs MockProductFrontEnd

    Returns
    -------
    list_products_ : list 
        list of product dictionaries
    result_dict : list or str
        Either: list of product dictionaries of most recent search
        Or: 'Goodbye!'
    """
    mock = MockProductFrontEnd()
    mock.welcome_message()
    mock.selecting_ingredients()
    list_products_ = mock.input_products()
    result_dict={}
    result_dict = mock.results_again()
    return list_products_,result_dict

if __name__ == '__main__':

    output = run()
