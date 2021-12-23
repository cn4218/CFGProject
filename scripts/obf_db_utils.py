#In[]
import mysql.connector
from pprint import pp 
import json
import pandas as pd
import math
import sys
from pathlib import Path


sys.path.append(str(Path(__file__).parent.parent.parent)) 

from CFGProject.scripts.config import USER, PASSWORD, HOST

## FUNCTIONS IN THIS SCRIPT:
"""
_connect_to_db(db_name)
_map_values(result)
exception_handler(query)
get_productids_containing(ingredient,n=None)
get_productids_ingt_in_nth_position(ingredient, n)
get_products_by_ids(id_list)
format_input(ingredients_input)
get_products(output,search_func1,search_func2)
get_proper_ingredients_list(_dict)
"""
## NOTE: I added the order in which the functions are called in this file (
# Ex: ## 3
#     def function(): ...
# so it is easier to follow our logic and the path of our data.
"""
NEW FUNCTIONS:
_get_all_product_ids
display_less_null_values
store_results
fetch_results
returning_products_in_pages
"""



# Required to handle database connection error exceptions
class DbConnectionError(Exception):
    pass


def _connect_to_db(db_name):
    """
    This establishes a connection to our database.
    :param db_name: Products
    :return: connection cnx
    """
    cnx = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        auth_plugin="mysql_native_password", 
        database=db_name,
    )
    return cnx


# NEED CLARIFICATION:
# Are we using this function? Where?
# Is 'brands' after 'quantity' somewhere?
# I simply reordered the item[i]s according to the column order
# in the cosmo_tables.sql DB file.
# + I replaced 'ingredients_list' with 'ingredients_text' as in the the cosmo_tables.sql DB file.
# Also there were some unwanted spaces between 'item' and '[i]' in places so I corrected that
def _map_values(result):
    """
    Transforms the (productID, code, product_name, ingredients_text, ...) item tuple result
    (19 elements) from cur.fetchall() into a list of dictionaries having values item[0-18].
    Depending on which information we want to display, we may only choose only a few columns
    or add more. For N columns we would have values item[0-(N-1)].
    If we select all columns (*) in our queries, N=19 so we have item[0-18].
    /!\ Pay attention to match the order of the columns in the queries with this list!
    --> We chose to select all fields here: SELECT *
    """
    mapped = []
    for item in result:
        mapped.append(
            {
               "productID": item[0],
                "code": item[1],
                "product_name": item[2],
                "ingredients_text": item[3],
                "brands": item[5],
                "quantity": item[4],
                "brands_tags": item[6],
                "categories": item[7],   # CHECK ORDER!!!
                "categories_tags": item[8],
                "categories_en": item[9],
                "countries": item[10],
                "countries_tags": item[11],
                "countries_en": item[12],
                "image_url": item[13],
                "image_small_url": item[14],
                "image_ingredients_url": item[15],
                "image_ingredients_small_url": item[16],
                "image_nutrition_url": item[17],
                "image_nutrition_small_url": item[18],
            }
        )
    return mapped

# Replaced the DB name 'external_obf_testing' by 'Products'
# to be consistent with the cosmo)_tables.sql DB file
# This exception handler can be adapted into 2 functions:
# 1. One to get all the productID's corresponding to products containing an ingredient
# 2. And the other that will get products based on their productID
## 4
def exception_handler(query): 
    """
    This function is the exception handler for exceptions that may arise when connecting
    to the database.
    """
    try:
        db_name = "Products"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)

        cur.execute(query) 
        result = (cur.fetchall())
        cur.close()

    except Exception as err:
        raise DbConnectionError("Failed to read data from DB",err)

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")

    return result  # SHOULDN'T WE INCREMENT THE SPACING HERE SO IT'S IN THE FINALLY BLOCK?


def _get_all_product_ids():
    """
    Function that returns all product ids from sql table products_table
    Returns
    --------
    id_list: list
        list of ids for all products"""
    query = """
    SELECT productID
    FROM products_table"""
    query_result = exception_handler(query)
    id_list = []
    for element in query_result:
        id_list.append(element[0]) # list of integers (productId's)
    
    return id_list    

# Replaced 'products1' by 'products_table' as in the cosmo_tables.sql DB file
## 3 / 3a
def get_productids_containing(ingredient, n=None):
    """
    This function takes an ingredient and searches through the Products.products_table
    table to find the rows that contain it, then it gets the productId's of those rows.
    Returns a list of productIDs.
    /!\ NOTE: There is a n parameter in this function that seems not to be used,
    but in reality it is necessary, because the function search_func2(ingredient,n)
    in the function #2 get_products(output,search_func1,search_func2) called by the
    function # 0 get_proper_ingredients_list(_dict)in the  of the 'filtered' parameter
    being 'ordered'... requires this parameter n.
    """
    query = """
            SELECT productID 
            FROM products_table
            WHERE ingredients_text LIKE '%{ing}%'
            """.format(
                ing=ingredient
            )
    query_result = exception_handler(query) # list of tuples     # 4
    id_list = []
    for element in query_result:
        id_list.append(element[0]) # list of integers (productId's)
    
    return id_list


## 3b
def get_productids_ingt_in_nth_position(ingredient, n):
    """
    This function creates a query to look in the ingredients_table table for products
    having a specific ingredient in the nth position (that is in their column named
    idx = (n-1)) and selects their productIDs.
    Returns a list of productIDs
    """

    idx = str(int(n) - 1)
    query = """
        SELECT productID 
        FROM ingredients_table
        WHERE `{idx}` LIKE '%{ing}%'  
        """.format(
            idx=idx,
            ing=ingredient
        )

    query_result = exception_handler(query)    # 4
    id_list = []
    for element in query_result:
        id_list.append(element[0]) # list of integers (productID's)
    return id_list


## 5
def get_products_by_ids(id_list):
    """
    This function creates a query that will be used to get rows if the productId of that 
    row is found in a record tuple of productIds.
    Returns a list of product dictionaries.
    """
    # converting to tuple() alone didn't work be cause the syntax of a tuple
    # with 1 single element conflicts with mysql. Eg: (96,)
    try:
        form_tup_string = "("
        length = len(id_list)
        for i in range(length):
            if i < length-1:
                form_tup_string += str(id_list[i]) + ","
            else:
                form_tup_string += str(id_list[i]) + ")"  

        query = """
                SELECT * FROM products_table  --  what is products1? products_table?
                WHERE productID IN 
                """
        query += form_tup_string
        # print(query)

        query_result = exception_handler(query)
        list_products = _map_values(query_result)

    except Exception:
        raise mysql.connector.ProgrammingError('Input value is an empty list')

    return list_products


## 1
def format_input(ingredients_input):
    """
    This takes the search dictionary input from the front end with the structure:
    {"1":["ingredient1",True], "2": ["ingredient2",False],.....,"5":["ingredient5",True]}
    and returns a list of tuples (i,k) where i =  ingredients and k = desired position 
    in ingredient list.
    When k = 0 it means that you want to exclude the corresponding ingredient.
    """
    ingredients_output = []
    for key,value in ingredients_input.items():
        ingredient,decision = value
        if ingredient: 
            if decision:
                tup = (ingredient.strip(), key)  
                ingredients_output.append(tup)
            else:
                tup = (ingredient.strip(), '0') 
                ingredients_output.append(tup)
    return ingredients_output 


## 2
def get_products(output,search_func1,search_func2): #both functions have to do with getting Id's
    """
    This function takes a list of productID's corresponding to the products that contain 
    ingredients you want to find (either unordered or in  specific positions) and include,
    as well as ingredients you don't want to include.
    It then finds the productID's corresponding to the products that have all the ingredients 
    you want first and foremost. Eg [[1,2,4,5,3], [5,4,3], [3,6,7,4,84,25,5]] -> [4,5,3]
    Then it makes sure that result does not contain a productID corresponding to a 
    product which contains an ingredient you do not want. For example, if you don't want 
    an ingredient found in the product that equals productID 4, then your final result would be [5,3]
    
    After it has created this list, it uses the get_products_by_ids() function to fetch the product info 
    for of every productID in your list
    """
    include = []
    exclude = []
    for pair in output:
        ingredient, n = pair
        if ingredient == '':  
            pass
        else:
            if n == '0':
            #    print("This is the ingredient we are searching",ingredient)
                exclude_list = search_func1(ingredient) 
                exclude.extend(exclude_list)  
                
            else: 
                include_list = search_func2(ingredient,n)  
                include.append(include_list)
    
    if include == []:    ## sophie: added this if else so that the results can show if only excludes are entered in search
        include = _get_all_product_ids()   ## gets all product ids 
        difference_exclude = list(set(include).difference(set(exclude)))   
    else:

        intersection_include = list(set.intersection(*map(set,include)))
        difference_exclude = list(set(intersection_include).difference(set(exclude)))
    try:
        if len(difference_exclude) == 0:
            issue = 'Query returns no search results'
            return Exception(issue)

    except Exception as err:
        print('Error raised: ',err)
        return err
    # print(difference_exclude)

    list_dict_products = get_products_by_ids(difference_exclude)

    return list_dict_products

# So we need to make sure empty fields don't display null but maybe NotAvailable. 
# We also need a function that pushes the products with a lot of null values to the bottom of the list being sent.

def display_less_null_values(input_list_dict_products):
    """
    Function edits input list dictionary of products, changes all null values to 'NotAvailable' 
    and sorts the list so that entries at the top have less null values.
    Parameters
    ----------
    input_list_dict_products: list
        list of product of dictionaries
    Returns
    --------
    list_dict_products_sorted: list
        list of product of dictionaries after sorting null values
    """
    df = pd.DataFrame(input_list_dict_products)
    df['null_count'] = df.isnull().sum(axis=1)
    df = df.sort_values('null_count')
    df.fillna('NotAvailable',inplace=True)
    df.pop('null_count')
    list_dict_products_sorted = df.to_dict(orient='records')
    return list_dict_products_sorted

## 0
def get_proper_ingredients_list(_dict):
    """
    This function receives a dictionary containing the users search ingredients and the type of search.
    The user is able to choose a search of type 'ordered' or 'unordered' and their choice is saved
    to the dict 'filter' key which we will access below.
    Then there is a key 'data' that holds a dictionary value in the format:
    {
        "1" : (ingredient1, True),
        "2": (ingredient2, True),
        "3": (ingredient3, True),
        "4": (ingredient4, False),
        "5": (ingredient5, True),
    }
    for example, where the ingredient input represents the ingredient the user wants to include/exclude
    and the boolean tells us whether to include the corresponding ingredient or not.
    ie True = include ingredient and False = exclude ingredient.
    The key values from 1 -> 5 signify the position the ingredients should be searched in if the user 
    set the 'filter' to ordered and otherwise the order of search is irrelevant. It is also important
    that whenever an ingredient has a corresponding boolean set to False, it means the user just doesn't want
    this ingredient anywhere in the product ingredient list, and so the search for that particular unwanted
    ingredient/set of ingredients is unordered and unaffected by the value of the 'filter' key
    The dict that holds the ingredient inputs is formatted with the format_input() function
    and the result of that is passed to the get_products() function which then returns a list of
    product dictionaries as our search results.
    """
    filtered = _dict['filter']
    ingredients_input = _dict['data']
    ingredients_output = format_input(ingredients_input)   # 1
    pp(ingredients_output)

    if filtered == 'unordered':
        list_products = get_products(     # 2
            ingredients_output,
            get_productids_containing,    # 3
            get_productids_containing     # 3
        ) 
        print(type(list_products))
        if isinstance(list_products,list):
            list_products = display_less_null_values(list_products)  
        ## sophie: returns list with product dictionarys with more null values at the end, replacing None with NotAvailable
        return list_products

    elif filtered == 'ordered':
        list_products = get_products(              # 2
            ingredients_output, 
            get_productids_containing,             # 3a
            get_productids_ingt_in_nth_position    # 3b
        )

        pp(list_products)
        if isinstance(list_products,list):
            list_products = display_less_null_values(list_products) 


        return list_products
        


        
def store_results(list_of_products):
    """
    This takes in a list of product ids retrieved from the search, turns the list into a dict and then into a string.
    The string is entered into a sql table within products database where its given an unique search id, (can also enter user id??)
    When inserted the search id created is retrieved and returned.
    Parameters
    -----------
    list_of_products: list
        list of product ids retrieved from search result
    """
    df = pd.DataFrame(list_of_products)
    product_ids = df['productID'].tolist()
    products_dictionary = {"product_ids": product_ids}

    products_dict_string = str(products_dictionary)
    try:
        db_name = "Products"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()

        print("Connected to DB: %s" % db_name)

        query_update = """
        UPDATE search_results
        SET list_product_id = "{}"
        WHERE search_id=1;
        """.format(products_dict_string)
        ## query retrieves the search id just created 
        cur.execute(query_update)
        db_connection.commit()

        cur.close()
        return products_dictionary
    except Exception as err:
        raise DbConnectionError("Failed to read data from DB",err)
    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")




def fetch_results(search_id):
    """
    This takes a search id and retrieves the string of dict of list of products from sql table.
    Formats it into a list and then puts into get_products_by_id function to return a list of dictionary products.
    Parameters
    -----------
    search_id: int
        identifier to search sql table and retrieve search results

    Returns
    --------
    list_dict_products: list
        list dicionary products of saved search result
    """
    list_dict_products = []
    try:
        query = """
        SELECT List_Product_ID FROM search_results WHERE Search_ID = {}""".format(search_id)
        query_result = exception_handler(query)
        query_dict = query_result[0][0].replace("'",'"')
        dict_product_ids = json.loads(query_dict)
        list_ids = dict_product_ids['product_ids']
        
        list_dict_products = get_products_by_ids(list_ids)
        list_dict_products = display_less_null_values(list_dict_products)

    except Exception:
        return IndexError('Query returns no search results, use search ID 1')


    return list_dict_products
def returning_products_in_pages(list_dict_products,page_number):
    """
    Function that divides list of product dictionaries into groups of 25
    page #: list slicing - # of results
    page 1: 0-25 --(1-24)
    page2: 25-50 -- (25-49)
    page3: 50-75 -- (50-74)
    Parameters
    -----------
    list_dict_products: list
        list of product dictionaries for a search result
    page_number: int
        page number being called in the search
    
    Returns
    ---------
    Either:
    products_list: list
        list of product dictionaries for given page number(will have length 25, unless its the last page)
    message: str
        message for when a page number is called thats larger than the max number of pages for a search result
        'No more search results for this query'
    """
    amount_products = len(list_dict_products)
    products_per_page = 25
    total_pages = math.ceil(amount_products/products_per_page)
    if page_number<=total_pages:
        upper_page = page_number*25
        lower_page = upper_page-25
        products_list = list_dict_products[lower_page:upper_page]
        return products_list
    else:
        message = 'No more search results for this query'
        return message


def verify_product_id(product_id):
    """
    This function takes in the product_id and searches all the product id's in the products table 
    to verify  the product_id. If it exists, it returns nothing, otherwise an exception is raised 
    """
    try:
        query = """
        SELECT * FROM 
        products_table WHERE productID = {}""".format(product_id)
        query_result = exception_handler(query)
        if len(query_result) == 0:
            issue = 'No result found for given product ID'
            raise Exception(issue)
    except Exception as err:
        raise Exception(err)
