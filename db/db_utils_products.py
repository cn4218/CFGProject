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
    Transforms (productID, product_name, ingredients_list) item tuple results
    (3 elements) from cur.fetchall() into a list of dictionaries having values item[0-2].
    Depending on which information we want to display, we may only choose these 3 columns
    or add more. For N columns we would have to values item[0-(N-1)].
    If we select all columns (*) in the queries, N=19 so we have item[0-18].
    /!\ Pay attention to match the order of the columns in the queries with this list!
    """
    mapped = []
    for item in result:
        mapped.append(
            {
                "productID": item[0],
                # "code": item[],
                "product_name": item[1],
                "ingredients_list": item[2]
                # "brands": item[],
                # "quantity": item[],
                # "brands_tags": item[],
                # "categories": item[],
                # "categories_tags": item[],
                # "categories_en": item[],
                # "countries": item[],
                # "countries_tags": item[],
                # "countries_en": item[],
                # "image_url": item[],
                # "image_small_url": item[],
                # "image_ingredients_url": item[],
                # "image_ingredients_small_url": item[],
                # "image_nutrition_url": item[],
                # "image_nutrition_small_url": item[],
            }
        )
    return mapped


def get_products_containing(ingredient):
    """ Returns a list of dictionaries of products containing a 
    specific ingredient in their ingredient_list (fuzzy search) """
    list_products = []
    try:
        db_name = "Products"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)

        query = f"""
            SELECT productID, product_name, ingredients_list   -- * ?
            FROM products_table 
            WHERE ingredients_list LIKE '%{ingredient}%'
            """

        cur.execute(query)
        # this is a list with db records where each record is a tuple
        result = (cur.fetchall())
        list_products = _map_values(result)  # not sure what to do about that
        cur.close()

    except Exception:
        raise DbConnectionError("Failed to read data from DB")

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")

    return list_products



def get_products_ingt_in_nth_position(ingredient,n):
    """ Returns a list of dictionaries of products containing a 
    specific ingredient in nth position in their ingredient_list 
    (fuzzy search) --> or exact search?"""
    list_products = []
    try:
        db_name = "Products"
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)

        # Nth position: N = index - 1
        # Ex: N = 1 --> i = 0      i = N + 1
        idx = str(int(n)+1)
       
        query = f"""
            SELECT p.productID, p.product_name, p.ingredients_list   -- *  ?
            FROM products_table AS p
            LEFT JOIN ingredients_table AS i
            ON p.productID = i.productID
            WHERE i.`{idx}` LIKE '%{ingredient}%'   --  = '{ingredient}'  ?
            ORDER BY p.productID ASC;    -- p.product_name ASC;  ?
            """

        cur.execute(query)
        # this is a list with db records where each record is a tuple
        result = (cur.fetchall())
        list_products = _map_values(result)  # not sure what to do about that
        cur.close()

    except Exception:
        raise DbConnectionError("Failed to read data from DB")

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")

    return list_products


if __name__ == "__main__":
    get_products_containing('glycerin')