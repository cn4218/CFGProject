import mysql.connector
from config import USER, PASSWORD, HOST
from pprint import pp 

#Functions in this script
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



#Chizu: uncommented this 
class DbConnectionError(Exception):
    pass


def _connect_to_db(db_name):
    cnx = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        auth_plugin="mysql_native_password", 
        database=db_name,
    )
    return cnx


def _map_values(result):
    mapped = []
    for item in result:
        mapped.append(
            {
               "productID": item[0],
                "code": item[1],
                "product_name": item[2],
                "ingredients_list": item[11],
                "brands": item[4], 
                "quantity": item[3], 
                "brands_tags": item[5], 
                "categories": item[7],
                "categories_tags": item[6], 
                "categories_en": item[7], 
                "countries": item [8],
                "countries_tags": item [9],
                "countries_en": item[10], 
                "image_url": item[12], 
                "image_small_url": item[13], 
                "image_ingredients_url": item[14], 
                "image_ingredients_small_url": item[15], 
                "image_nutrition_url": item[16], 
                "image_nutrition_small_url": item[17], 
            }
        )
    return mapped

#this can be adapted into 2 functions we need:
# 1. One to get all the productId's corresponding to products that contain the ingredient we want.
# 2. And the other that will get products based on the Id you give it.

def exception_handler(query): 
    """This function is the exception handler for exceptions that may arise when connecting to the 
    db """
    try:
        db_name = "external_obf_testing"
        db_connection = _connect_to_db( db_name )
        cur = db_connection.cursor()
        print( "Connected to DB: %s" % db_name )

        cur.execute(query) 
        result = (cur.fetchall())
        cur.close()

    except Exception:
        raise DbConnectionError( "Failed to read data from DB" )

    finally:
        if db_connection:
            db_connection.close()
            print( "DB connection is closed" )
    return result



def get_productids_containing(ingredient,n=None): #works
    """ This function takes an ingredient and searches through the products1
        table to find the rows that contain a specific ingredient.
        Then it gets the productId's of those rows. 
        Returns a list of productIDs 
    """
    query = """
            SELECT productID 
            FROM products1
            WHERE ingredients_text LIKE '%{ing}%'
            """.format(
                ing=ingredient
            )
    query_result = exception_handler(query) #list of tuples 
    id_list = []
    for element in query_result:
        id_list.append(element[0]) #list of integers (productId's)
    
    return id_list



def get_productids_ingt_in_nth_position(ingredient, n):
    """ This function creates a query to look for an ingredient in the nth position of 
    the id_ingredients1 table and it then gets the corresponding productIDs 
        Returns a list of productIDs 
    """

    idx = str( int( n ) - 1 )
    query = """
        SELECT productID 
        FROM id_ingredients1 
        WHERE `{idx}` LIKE '%{ing}%'  
        """.format(
            idx=idx,
            ing=ingredient
        )

    query_result = exception_handler(query)
    id_list = []
    for element in query_result:
        id_list.append(element[0]) #list of integers (productId's)
    return id_list

def get_products_by_ids(id_list):
    """
    This function creates a query that will be used to get rows if the productId of that 
    row is in  found in a record tuple of productIds.
    Returns a list of product dictionaries 
    """
    form_tup_string = "(" #converting to tupe() alone didn't work cause the syntac of a tuple with 1 elements conflicts with mysql eg (96,)
    length = len(id_list)
    for i in range(length):
        if i < length-1:
            form_tup_string += str(id_list[i]) + ","
        else:
            form_tup_string += str(id_list[i]) + ")"  

    query = """
            SELECT * FROM products1
            WHERE productID IN 
            """
    query += form_tup_string
   # print(query)

    query_result = exception_handler(query)
    list_products = _map_values(query_result)
    return list_products


def format_input(ingredients_input):  # Chizu's function modified by Claire
    """ This takes a dictionary input with the structure:
    {"1":["ingredient1",True], "2": ["ingredient2",False],.....,"5":["ingredient5",True]}
    and returns a list of tuples (i,k) where i =  ingredients and k = desired position 
    in ingredient list. when k = 0 it means you don't want to include the corresponding ingredient.
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


def get_products(output,search_func1,search_func2): 
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
    
   

    intersection_include = list(set.intersection(*map(set,include)))
    difference_exclude = list(set(intersection_include).difference(set(exclude)))

    # print(exclude)
    # print(include)
    # print(intersection_include)
   # print(difference_exclude)

    list_dict_products = get_products_by_ids(difference_exclude)
   # print(list_dict_products)
    
    return list_dict_products

def get_proper_ingredients_list(_dict):
    """
    This function receives a dictionary containing the users search ingredients and the type of search.
    The user is able to choose a search of type ordered or unordered and their choice is saved to the dict "filter"
    key which we will access below. 

    Then there is a key "data" that holds a dictionary value in the format 
    {
        "1" : (ingredient1, True),
        "2": (ingredient2, True),
        "3": (ingredient3, True),
        "4": (ingredient4, False),
        "5": (ingredient5, True),

    }
    for example, where the ingredient input represents the ingredient the user wants to include/not 
    include and the boolean tells us whether to include the corresponding ingredient or not. 
    ie True = include ingredient and False = don't include ingredient.

    The key values from 1 -> 5 signify the position the ingredients should be searched in if the user 
    set the "filter" to ordered and otherwise the order of search is irrelevant. It is also important 
    that whenever an ingredient has a corresponding boolean set to False. It means the user just doesn't want 
    this ingredient anywhere in the product ingredient list and so the search for that particular unwanted
    ingredient/set of ingredients is unordered and unaffected by the value of the "filter" key 

    The dict that holds the ingredient inputs are formatted with the format_input() function 
    and the result of that is passed to the get products function which then returns a list of 
    product dictionaries as our search results. 

    """
    filtered = _dict['filter']
    ingredients_input = _dict['data']
    ingredients_output = format_input(ingredients_input)
    pp(ingredients_output)

    if filtered == 'unordered':
        list_products = get_products(
            ingredients_output,
            get_productids_containing, 
            get_productids_containing
        ) 
        return list_products 

    elif filtered == 'ordered':
        list_products = get_products(
            ingredients_output, 
            get_productids_containing, 
            get_productids_ingt_in_nth_position
        )
        return list_products 
        


























#tests
#output = [('poudre de maranta arundinacea (marante)','1'), ('bicarbonate de sodium','2'), ('huile de cocos nucifera (noix de coco)' , '3'),('caprylic/capric triglyceride','0') , ('butyrospermum parkii (beurre de karité)','4')]


#get_products(output,get_productids_containing,get_productids_ingt_in_nth_position)


"""
Test: 
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

Got expected result: 
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
'ingredients_list': "poudre de maranta arundinacea (marante), bicarbonate de sodium, 
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






















