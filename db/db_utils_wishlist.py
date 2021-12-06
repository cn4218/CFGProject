"""IGNORE!!!"""
### IGNORE THIS FILE, AS WE WILL BE USING NASIANS wishlist_db_utils.py

import mysql.connector
from mysql.connector import Error
from config import user_name, user_password, host_name


class DbConnectionError(Exception):
    pass

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host = host_name,
            user = user_name,
            password = user_password,
            database = db_name
        )
        print("MySQL Database Connection is Successful")
    except Error as er:
        print(f"Error: '{er}'")
    return connection


def _map_values(wish_list):
    mapped = []
    for item in wish_list:
        mapped.append(
            {
                "Product ID": item[0],
                "Product name": item[1],
                "Brands": item[2],
                "Countries": item[3],
                "Ingredients": item[4]
            }
        )
    return mapped

def get_all_wishlist(user_id):
    print(user_id)
    wishlist = []
    try: 
        db_name = 'wish_list'
        db_connection = create_db_connection(host_name, user_name, user_password, db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)

        query = """
            SELECT productID, product_name, brands, countries, ingredients_text
            FROM Wish_List
            WHERE User_ID = '{}'""".format(user_id)

        cur.execute(query)

        result = (
            cur.fetchall()
        )
        wishlist = _map_values(result)
        cur.close()
    except Exception as e:
        raise DbConnectionError("Failed to read data from DB",e)

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")

    return wishlist

def get_product_info(product_id):
    product_info = []
    try: 
        db_name = 'Products'
        db_connection = create_db_connection(host_name, user_name, user_password,db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)

        query = """
        SELECT User_ID, productID, code, product_name, quantity, brands, brands_tags, categories_tags, categories_en, 
        countries, countries_tags, countries_en, ingredients_text, image_url, image_small_url, image_ingredients_url, 
        image_ingredients_small_url, image_nutrition_url, image_nutrition_small_url
        FROM products_table 
        WHERE productID = '{}'""".format(product_id)

        cur.execute(query)

        result = (
            cur.fetchall()
        )
        product_info_tuple = result
        product_dict = _map_values(result)
        cur.close()


    except Exception:
        raise DbConnectionError("Failed to read data from DB")

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")

    return product_info_tuple

def add_wishlist_item(UserID, ProductID, Code_Wish, Product_name, Quantity, 
        Brands, Brands_tags, Categories_Tags, Countries_en, Ingredients_Text, Image_url, Image_Small_url, Image_Ingredients_url, 
        Image_Ingredients_Small_url, Image_Nutrition_url, Image_Nutrition_Small_url):

    try: 
        db_name = 'wish_list'
        db_connection = create_db_connection(host_name, user_name, user_password,db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)

        query = """
        INSERT INTO Wish_List (User_ID, productID, code, product_name, quantity, brands, brands_tags, categories_tags, categories_en, 
        countries, countries_tags, countries_en, ingredients_text, image_url, image_small_url, image_ingredients_url, 
        image_ingredients_small_url, image_nutrition_url, image_nutrition_small_url) VALUES ('{UserID}', '{ProductID}', '{Code_Wish}', '{Product_name}', '{Quantity}', 
        '{Brands}', '{Brands_tags}', '{Categories_Tags}', '{Countries_en}', '{Ingredients_Text}', '{Image_url}', '{Image_Small_url}', '{Image_Ingredients_url}', 
        '{Image_Ingredients_Small_url}', '{Image_Nutrition_url}', '{Image_Nutrition_Small_url}');
        """
        cur.execute(query)
        db_connection.commit()
        cur.close()
    except Exception as e:
        raise DbConnectionError("Failed to read data from DB",e)
    finally:
        if db_connection:
            db_connection.close()
def delete_wishlist_item(user_id, product_id):
    try:
        empty_list = []
        db_name = 'wish_list'
        db_connection = create_db_connection(host_name, user_name, user_password,db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)

        query = """
        DELETE FROM Wish_List 
        WHERE User_ID = {} and productID ={};
        """.format(user_id, product_id)

        cur.execute(query)
        db_connection.commit()
        cur.close()
    except Exception as e:
        raise DbConnectionError("Failed to read data from DB",e)
    finally:
        if db_connection:
            db_connection.close()

    return empty_list


def delete_wishlist(user_id):
    try:
        empty_list = []
        db_name = 'wish_list'
        db_connection = create_db_connection(host_name, user_name, user_password,db_name)
        cur = db_connection.cursor()
        print("Connected to DB: %s" % db_name)

        query = """
        DELETE FROM Wish_List 
        WHERE User_ID = {};
        """.format(user_id)

        cur.execute(query)
        db_connection.commit()
        cur.close()
    except Exception as e:
        raise DbConnectionError("Failed to read data from DB",e)
    finally:
        if db_connection:
            db_connection.close()

    return empty_list

if __name__ == '__main__':
    add_wishlist_item(1,2,3,4,5,6,7,8,9,10,11,23,14,15,16,17)
