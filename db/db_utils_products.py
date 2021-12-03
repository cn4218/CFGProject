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
    Transforms (productID, product_name, ingredients_list) tuples 
    results from cur.fetchall() into a list of dictionaries.
    """
    mapped = []
    for item in result:
        mapped.append(
            {
                "productID": item[0],
                "product_name": item[1],
                "ingredients_list": item[2]
            }
        )
    return mapped


def get_products_containing(ingredient):
    """ Returns a list of products as dictionaries """
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


if __name__ == "__main__":
    get_products_containing('glycerin')