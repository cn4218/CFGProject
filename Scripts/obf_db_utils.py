import mysql.connector
from config import USER, PASSWORD, HOST
from pprint import pp 

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
                "brands": item[4], 
                "quantity": item[5],
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
        db_name = "external_obf_testing"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)

        cur.execute(query) 
        result = (cur.fetchall())
        cur.close()

    except Exception:
        raise DbConnectionError("Failed to read data from DB")

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")
    return result  # SHOULDN'T WE INCREMENT THE SPACING HERE SO IT'S IN THE FINALLY BLOCK?


# Replaced 'products1' by 'products_table' as in the cosmo_tables.sql DB file
## 3 / 3a
def get_productids_containing(ingredient, n=None): # WHY IS n NOT USED IN THE FUNCTION?
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
def get_products(output,search_func1,search_func2): 
    """
    This function takes a list of productID's corresponding to the products that contain 
    ingredients you want to find (either unordered or in  specific positions) and include,
    as well as ingredients you want to exclude.

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
                # print("This is the ingredient we are searching:",ingredient)
                exclude_list = search_func1(ingredient) 
                exclude.extend(exclude_list)  
                
            else: 
                include_list = search_func2(ingredient,n)  
                include.append(include_list)

    intersection_include = list(set.intersection(*map(set,include)))
    difference_exclude = list(set(intersection_include).difference(set(exclude)))

    # print(exclude)
    # print(include)
    # print(intersection_include)
    # print(difference_exclude)

    list_dict_products = get_products_by_ids(difference_exclude)   # 5
    # print(list_dict_products)
    
    return list_dict_products


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
        return list_products 

    elif filtered == 'ordered':
        list_products = get_products(              # 2
            ingredients_output, 
            get_productids_containing,             # 3a
            get_productids_ingt_in_nth_position    # 3b
        )
        return list_products



##########################################################################
##########################################################################

# TESTS
# output = [('poudre de maranta arundinacea (marante)','1'), ('bicarbonate de sodium','2'), ('huile de cocos nucifera (noix de coco)' , '3'),('caprylic/capric triglyceride','0') , ('butyrospermum parkii (beurre de karité)','4')]

# get_products(output,get_productids_containing,get_productids_ingt_in_nth_position)


"""
TEST: 
_dict = {
    "filter": "ordered",
    "data": {
       "1": ('poudre de maranta arundinacea (marante)',True),
       "2": ('bicarbonate de sodium',True),
       "3": ('huile de cocos nucifera (noix de coco)' , True),
       "4": ('butyrospermum parkii (beurre de karité)',True),
       "5": ('caprylic/capric triglyceride',False)
    }
}

print(get_proper_ingredients_list(_dict))

GOT EXPECTED RESULT: 
[('poudre de maranta arundinacea (marante)', '1'), ('bicarbonate de sodium', '2'), ('huile de cocos nucifera (noix de coco)', '3'), ('butyrospermum parkii (beurre de karité)', '4'), ('caprylic/capric triglyceride', '0')]
Connected to DB: external_obf_testing
DB connection is closed
Connected to DB: external_obf_testing
DB connection is closed
Connected to DB: external_obf_testing
DB connection is closed
Connected to DB: external_obf_testing
DB connection is closed
Connected to DB: external_obf_testing
DB connection is closed
Connected to DB: external_obf_testing
DB connection is closed

[{'productID': 96, 'code': '19962085116', 
'product_name': 'Déodorant naturel', 
'ingredients_text': "poudre de maranta arundinacea (marante), bicarbonate de sodium, 
huile de cocos nucifera (noix de coco), butyrospermum parkii (beurre de karité), 
triglycéride caprylique / caprique (huile de coco fractionnée), cire d'euphorbia cerifera (candelilla),
huile de graines de simmondsia chinensis (jojoba)provenant du tournesol (vitamine e, provenant du tournesol)", 
'brands': "Schmidt's", 
'quantity': '92g', 
'brands_tags': 'schmidt-s', 
'categories': 'Hygiene,Deodorants', 
'categories_tags': 'en:hygiene,en:deodorants', 
'categories_en': 'Hygiene,Deodorants', 
'countries': 'France', 'countries_tags': 'en:france', 
'countries_en': 'France', 
'image_url': '', 
'image_small_url': '', 
'image_ingredients_url': '',
'image_ingredients_small_url': '', 
'image_nutrition_url': '', 
'image_nutrition_small_url': ''}]
"""






















