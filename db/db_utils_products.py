# db_utils_products

import mysql.connector
from config import USER, PASSWORD, HOST


class DbConnectionError(Exception):
    pass


def _connect_to_db(db_name):
    cnx = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        # auth_plugin="mysql_native_password",
        database=db_name,
    )
    return cnx


def _map_values(result):
    """
    Example: Transforms (productID, product_name, ingredients_list) item tuple results
    (3 elements) from cur.fetchall() into a list of dictionaries having values item[0-2].
    Depending on which information we want to display, we may only choose these 3 columns
    or add more. For N columns we would have to values item[0-(N-1)].
    If we select all columns (*) in the queries, N=19 so we have item[0-18].
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
                "ingredients_list": item[3],
                "brands": item[4],
                "quantity": item[5],
                "brands_tags": item[6],
                "categories": item[7],
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

def get_all_products():
    """ Returns a list of dictionaries for all products """
    list_products = []
    try:
        db_name = "Products"
        db_connection = _connect_to_db( db_name )
        cur = db_connection.cursor()
        print( "Connected to DB: %s" % db_name )

        query = "SELECT * FROM products_table;"

        cur.execute(query)
        # This is a list with db records where each record is a tuple with as
        # many elements as columns you selected in your query
        result = (cur.fetchall())
        list_products = _map_values(result)
        cur.close()

    except Exception:
        raise DbConnectionError( "Failed to read data from DB" )

    finally:
        if db_connection:
            db_connection.close()
            print( "DB connection is closed" )

    return list_products

def get_products_containing(ingredient):
    """ Returns a list of dictionaries of products containing a
    specific ingredient in their ingredient_list (fuzzy search) """
    list_products = []
    try:
        db_name = "Products"
        db_connection = _connect_to_db( db_name )
        cur = db_connection.cursor()
        print( "Connected to DB: %s" % db_name )

        query = f"""
            SELECT * 
            FROM products_table 
            WHERE ingredients_list LIKE '%{ingredient}%'
            """

        cur.execute(query)
        # This is a list with db records where each record is a tuple with as
        # many elements as columns you selected in your query
        result = (cur.fetchall())
        list_products = _map_values(result)
        cur.close()

    except Exception:
        raise DbConnectionError( "Failed to read data from DB" )

    finally:
        if db_connection:
            db_connection.close()
            print( "DB connection is closed" )

    return list_products


def get_products_not_containing(ingredient):
    """ Returns a list of dictionaries of products NOT containing a
    specific ingredient in their ingredient_list (fuzzy search)
    This would appear as .../ingredient/0... in the route """
    list_products = []
    try:
        db_name = "Products"
        db_connection = _connect_to_db( db_name )
        cur = db_connection.cursor()
        print( "Connected to DB: %s" % db_name )

        query = f"""
            SELECT *
            FROM products_table 
            WHERE ingredients_list NOT LIKE '%{ingredient}%'
            """

        cur.execute( query )
        # This is a list with db records where each record is a tuple with as
        # many elements as columns you selected in your query
        result = (cur.fetchall())
        list_products = _map_values( result )  # not sure what to do about that
        cur.close()

    except Exception:
        raise DbConnectionError( "Failed to read data from DB" )

    finally:
        if db_connection:
            db_connection.close()
            print( "DB connection is closed" )

    return list_products


def get_products_ingt_in_nth_position(ingredient, n):
    """ Returns a list of dictionaries of products containing a
    specific ingredient in Nth position in their ingredient_list
    (fuzzy search) --> or exact search? """
    list_products = []
    try:
        db_name = "Products"
        db_connection = _connect_to_db( db_name )
        cur = db_connection.cursor()
        print( "Connected to DB: %s" % db_name )

        # Nth position: N = index - 1
        # Ex: N = 1 --> i = 0      i = N + 1
        idx = str( int( n ) + 1 )

        query = f"""
            SELECT * 
            FROM products_table AS p
            LEFT JOIN ingredients_table AS i
            ON p.productID = i.productID
            WHERE i.`{idx}` LIKE '%{ingredient}%'   
            ORDER BY p.productID ASC;
            """

        cur.execute( query )
        # This is a list with db records where each record is a tuple with as
        # many elements as columns you selected in your query
        result = (cur.fetchall())
        list_products = _map_values( result )  # not sure what to do about that
        cur.close()

    except Exception:
        raise DbConnectionError( "Failed to read data from DB" )

    finally:
        if db_connection:
            db_connection.close()
            print( "DB connection is closed" )

    return list_products


# # ### Received request format (ingredient_input):
# input = {
#     'filter': 'ordered',
#     'data': {'1': ['water', True],
#              '2': ['glycerin ', False],
#              '3': ['alcohol', True],
#              '4': ['parfum', True],
#              '5': ['', True]
#              }
# }

def get_proper_ingredients_list(_dict):
    """
    1) FIRST this function receives the ingredients_input dictionary and format it with format_input(ingredients_input)
    2) THEN A) If it is 'unordered' it sends it to get_products_unordered()
            B) If it is 'ordered' it sends it to get_products_multi_criteria_search()
    """
    filtered = _dict['filter']
    ingredients_input = _dict['data']
    ingredients_output = format_input(ingredients_input)

    if filtered == 'unordered':
        list_products = get_products_unordered(ingredients_output)
        return list_products # List of product dictionaries

    elif filtered == 'ordered':
        list_products = get_products_multi_criteria_search(ingredients_output)
        return list_products # List of product dictionaries


def format_input(ingredients_input):  # Chizu's function modified by Claire
    """ This takes a dictionary input in the structure
    {"1":["ingredient1",True], "2": ["ingredient2",False],.....,"5":["ingredient5",True]}
    and returns a list containing tuples with ingredients to include (key number) or not (0)
    """
    ingredients_output = []
    for key,value in ingredients_input.items():
        ingredient,decision = value
        # if decision = True it means include ingredient, otherwise don't include
        if ingredient: # if not empty string
            if decision:
                tup = (ingredient.strip(), key)  # strips leading and trailing spaces
                ingredients_output.append(tup)
            else:
                tup = (ingredient.strip(), '0')  # position '0' means 'not included'
                ingredients_output.append(tup)
    return ingredients_output   # List of tuples


# ### Transmitted request format (ingredients_output):
# ingredients_output = [('water','1'),('glycerin','0'),('alcohol','3'),('parfum','4'),('','5')]


# IF UNORDERED ####################
def get_products_unordered(output):
    include = []
    exclude = []
    for pair in output:
        ingredient, n = pair
        if ingredient == '':   # skip empty string ingredients
            pass
        else:
            if n == '0':
                # Strategy 1: exclude X = [products with X] --> [4]
                exclude_list = get_products_containing(ingredient)
                exclude.append(exclude_list)

                # (abandoned, too long)
                # Strategy 2: intersect with ∁X = [products without X] --> ∁[4]
                # exclude_list = get_products_not_containing(ingredient)
                # exclude.extend(exclude_list)

            else: # List of lists of products containing the given ingredients
                include_list = get_products_containing(ingredient)
                include.append(include_list)
                # Example: I = A ∪ B ∪ C  -->  [[1,2,3,4,5,6,7],[1,3,4,5,8],[2,4,5,9]]

    # Intersection of lists for included ingredients: II = A ∩ B ∩ C  -->  [4,5]
    intersection_include = list(set.intersection(*map(set,include)))

    # Strategy 1: exclude X = [products with X] --> III = II ∆ X --> [5]
    difference_exclude = list(set(intersection_include).difference(set(exclude)))
    return difference_exclude    # III = (A ∩ B ∩ C) ∆ X

    # Strategy 2: intersect with ∁X = [products without X] --> III = II ∩ ∁X --> [5]
    # intersection_exclude =  list(set(intersection_include).intersection(set(exclude)))
    # return intersection_exclude    # III = (A ∩ B ∩ C) ∩ ∁X


# IF ORDERED ##################################
def get_products_multi_criteria_search(output):
    include = []
    exclude = []
    for pair in output:
        ingredient, n = pair
        if n == '0':
            # Strategy 1: exclude X = [products with X] --> [4]
            exclude_list = get_products_containing(ingredient)
            exclude.append(exclude_list)

            # (abandoned, too long)
            # Strategy 2: intersect with ∁X = [products without X] --> ∁[4]
            # exclude_list = get_products_not_containing(ingredient)
            # exclude.extend(exclude_list)

        else: # List of lists of products containing the given ingredients in nth position
            include_list = get_products_ingt_in_nth_position(ingredient, n)
            include.append(include_list)
            # Example: I = A1 ∪ B2 ∪ C3  -->  [[1,2,3,4,5,6,7],[1,3,4,5,8],[2,4,5,9]]

    # Intersection of lists for included ingredients: II = A1 ∩ B2 ∩ C3  -->  [4,5]
    intersection_include = list(set.intersection(*map(set,include)))

    # Strategy 1: exclude X = [products with X] --> III = II ∆ X --> [5]
    difference_exclude = list(set(intersection_include).difference(set(exclude)))
    return difference_exclude    # III = (A1 ∩ B2 ∩ C3) ∆ X

    # Strategy 2: intersect with ∁X = [products without X] --> III = II ∩ ∁X --> [5]
    # intersection_exclude =  list(set(intersection_include).intersection(set(exclude)))
    # return intersection_exclude    # III = (A1 ∩ B2 ∩ C3) ∩ ∁X


#############
# ### Received request format (ingredient_input):
input = {
    'filter': 'ordered',
    'data': {'1': ['water', True],
             '2': ['glycerin ', False],
             '3': ['alcohol', True],
             '4': ['parfum', True],
             '5': ['', True]
             }
}
print(input)
print(format_input(input['data']))

# def format_input(ingredient_input):   # Chizu's function
#     # need to make sure white spaces are removed before they are sent over the api
#     """ This takes a dictionary input in the structure
#     {"1":["ingredient1",True], "2": ["ingredient2",False],.....,"5":["ingredient5",True]}
#     and creates a dictionary of 2 list values containing ingredients to include and not to include
#     """
#     ingredient_list = []
#     not_ingredient_list = []
#     for key,value in ingredient_input.items():
#         ingredient,decision = value
#         # if decision = True it means include ingredient, otherwise don't include
#         if ingredient: # if not empty string
#             if decision:
#                 tup = (key,ingredient)
#                 ingredient_list.append(tup)
#             else:
#                 not_ingredient_list.append(ingredient)
#     return {"included": ingredient_list, "not_included": not_ingredient_list}


#
# if __name__ == "__main__":
#     get_products_containing('glycerin')
